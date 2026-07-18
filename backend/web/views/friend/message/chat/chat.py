import asyncio
import base64
import os
import ssl
from queue import Queue
import threading
from typing import Any

import certifi

from django.http import StreamingHttpResponse
from django.db.models import Subquery
from pprint import pprint

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import BaseRenderer
from rest_framework.permissions import IsAuthenticated

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from websockets import ClientConnection
import websockets

from web.views.friend.message.memory.update import update_memory
from web.models.friend import Friend, Message, SystemPrompt
from web.views.friend.message.chat.graph import ChatGraph

import json
import logging
logger = logging.getLogger(__name__)


class SSERenderer(BaseRenderer):
    media_type = "text/event-stream"
    format = "txt"
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

def add_system_prompt(state, friend: Friend):
    msgs = state['messages']
    system_prompts = SystemPrompt.objects.filter(title='回复').order_by('order_number')
    prompt = ''
    for sp in system_prompts:
        prompt += sp.prompt
    prompt += f'\n【角色性格】\n{friend.character.desc}\n'
    prompt += f'\n【长期记忆】\n{friend.memory}\n'
    return {"messages" : [SystemMessage(prompt)] + msgs}
    
def add_recent_messages(state, friend: Friend):
    msgs = state['messages']
    latest_message_ids = Message.objects.filter(friend=friend).order_by('-id')[:10].values('id')
    messages_raw = list(Message.objects.filter(id__in=Subquery(latest_message_ids)).order_by('id'))
    messages = []
    for m in messages_raw:
        messages.append(HumanMessage(m.user_message))
        messages.append(AIMessage(m.output))
    
    return {"messages" : msgs[:1] + messages + msgs[-1:]}

class MesssageChatView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes =[SSERenderer]

    def post(self, request: Request):
        try:
            friend_id = request.data["friend_id"]
            message = request.data.get("message").strip()
            if not message:
                return Response({ 'result' : '消息不能为空' }, status=400)
            
            friends = Friend.objects.filter(pk=friend_id, me__user=request.user)
            if not friends.exists():
                return Response({ 'result' : '好友不存在' }, status=400)
            friend = friends.first()

            app = ChatGraph.create_app()
            inputs = {
                "messages" : [HumanMessage(content=message)],
            }
            inputs = add_system_prompt(inputs, friend)
            inputs = add_recent_messages(inputs, friend)
            # pprint(inputs)

            response = StreamingHttpResponse(
                self.event_stream(app, inputs, friend, message), 
                content_type="text/event-stream"
            )
            response['Cache-control'] = "no-cache"
            return response
        except Exception as e:
            logger.exception(e)
            return Response({ 'result' : '系统异常，请稍后重试' }, status=500)
    
    async def tts_sender(self, app, inputs: dict[str, Any], mq: Queue, ws: ClientConnection):
        usage: dict[str, int] = {}
        async for msg, _ in app.astream(inputs, stream_mode="messages"):
            if isinstance(msg, AIMessage) and msg.content:
                mq.put_nowait({"content" : msg.content})

                # Stream text chunk upwards (text bytes in)
                text_frame = {
                    "text": msg.content,
                    "try_trigger_generation": True
                }
                await ws.send(json.dumps(text_frame))
            
                if msg.usage_metadata:
                    # Gemini streams usage as per-chunk deltas, so sum them
                    for k in ("input_tokens", "output_tokens", "total_tokens"):
                        usage[k] = usage.get(k, 0) + msg.usage_metadata.get(k, 0)
        
        mq.put_nowait({"usage" : usage})
        # Send an empty block to finish compilation
        await ws.send(json.dumps({"text" : ""}))

    async def tts_receiver(self, mq: Queue, ws: ClientConnection):
        try:
            async for message in ws:
                data = json.loads(message)
                
                # Capture generated voice bytes (Whiteboard: audio bytes out)
                if data.get("audio"):
                    audio_bytes = base64.b64decode(data["audio"])
                    # Forward base64 payload to your main SSE queue
                    mq.put_nowait({"audio" : base64.b64encode(audio_bytes).decode('utf-8')})
                    
                if data.get("isFinal"):
                    break
        except Exception as e:
            logger.error(e)

    async def run_tts_tasks(self, app, inputs: dict[str, Any], mq: Queue) -> None:
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        voice_id = os.environ.get("ELEVENLABS_VOICE_ID")
        model_id = os.environ.get("ELEVENLABS_MODEL_ID")

        wss_url = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id={model_id}"

        # ElevenLabs validates using custom header field
        headers = {"xi-api-key": api_key}

        # some Python installs (macOS python.org builds) ship without a default CA bundle wired up
        # pin to certifi's explicitly rather than relying on the system trust store
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with websockets.connect(wss_url, additional_headers=headers, ssl=ssl_context) as ws:
            # 1. Init connection
            init_frame = {
                "text": " ",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "use_speaker_boost": False
                },
                "generation_config": {
                    "chunk_length_schedule": [120, 160, 250, 290]
                }
            }
            await ws.send(json.dumps(init_frame))

            # 2. Parallel full-duplex stream
            await asyncio.gather(
                self.tts_sender(app, inputs, mq, ws),
                self.tts_receiver(mq, ws)
            )
     

    def worker(self, app, inputs: dict[str, Any], mq: Queue) -> None:
        try:
            asyncio.run(self.run_tts_tasks(app, inputs, mq))
        except Exception as e:
            logger.error(e)
        finally:
            mq.put_nowait(None) # ending flag
    
    def event_stream(self, app, inputs: dict[str, Any], friend: Friend, message: str):
        mq = Queue()
        thread = threading.Thread(target=self.worker, args=(app, inputs, mq))
        thread.start()

        full_output = ''
        full_usage = {}
        while True:
            msg = mq.get()
            # print(msg)
            if not msg:
                break
            if msg.get('content', None):
                full_output += msg['content']
                yield f"data: {json.dumps({"content" : msg['content']}, ensure_ascii=False)}\n\n"
            if msg.get('audio', None):
                yield f"data: {json.dumps({"audio" : msg['audio']}, ensure_ascii=False)}\n\n"
            if msg.get('usage', None):
                full_usage = msg['usage']
        
        yield "data: [DONE]\n\n"
        input_tokens = full_usage.get("input_tokens", 0)
        output_tokens = full_usage.get("output_tokens", 0)
        total_tokens = full_usage.get("total_tokens", 0)

        Message.objects.create(
            friend=friend,
            user_message=message[:500],
            inputs=json.dumps([m.model_dump() for m in inputs["messages"]], ensure_ascii=False),
            output=full_output,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens
        )

        if Message.objects.filter(friend=friend).count() % 10 == 0: # change to 10 in prod
            update_memory(friend)
