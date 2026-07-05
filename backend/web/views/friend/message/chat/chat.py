from django.http import StreamingHttpResponse
from django.db.models import Subquery
from pprint import pprint

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import BaseRenderer
from rest_framework.permissions import IsAuthenticated

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage

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
    renderer_classes=[SSERenderer]
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

            def event_stream():
                full_output = ''
                full_usage = {}
                for msg, metadata in app.stream(inputs, stream_mode="messages"):
                    if isinstance(msg, BaseMessage):
                        if msg.content:
                            full_output += msg.content
                            yield f"data: {json.dumps({"content" : msg.content}, ensure_ascii=False)}\n\n"
                        if hasattr(msg, "usage_metadata") and msg.usage_metadata:
                            # Gemini streams usage as per-chunk deltas, so sum them
                            for k in ("input_tokens", "output_tokens", "total_tokens"):
                                full_usage[k] = full_usage.get(k, 0) + msg.usage_metadata.get(k, 0)
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
            
            response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
            response['Cache-control'] = "no-cache"
            return response
        except Exception as e:
            logger.exception(e)
            return Response({ 'result' : '系统异常，请稍后重试' }, status=500)
