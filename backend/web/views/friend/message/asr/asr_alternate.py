import json
import os
from typing import Any, Dict
import uuid

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import asyncio
import websockets
from websockets.asyncio.client import ClientConnection

import logging
logger = logging.getLogger(__name__)

class ASRModelView(APIView):
    """
    A specialized version of asr.py designed to call Aliyun's Gummy ASR model.

    :doc https://bailian.console.aliyun.com/cn-beijing/?spm=5176.12818093_47.console-base_product-drawer-right.dproducts-and-services-sfm.258b16d0dZyCzu&tab=api#/api/?type=model&url=2869339
    """
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        audio = request.FILES.get('audio')
        if not audio:
            return Response({ 'result' : '音频不存在' }, status=400)

        pcm_data = audio.read()
        if (len(pcm_data) < 2) or (len(pcm_data) % 2 != 0):
            return Response({'result': '音频格式错误'}, status=400)
        
        text = asyncio.run(self.run_asr_tasks(pcm_data))

        return Response({'result' : 'success', 'text' : text}, status=200)
    
    async def asr_sender(self, pcm_data: bytes, ws: ClientConnection, task_id: str):
        chunk = 3200
        for i in range(0, len(pcm_data), chunk):
            await ws.send(pcm_data[i : i + chunk])
            await asyncio.sleep(0.01)
        await ws.send(json.dumps({
            "header": {
                "action": "finish-task",
                "task_id": task_id,
                "streaming": "duplex"
            },
            "payload": {
                "input": {}
            }
        }))

    async def asr_receiver(self, ws: ClientConnection) -> str:
        text = ''
        async for msg in ws:
            response = json.loads(msg)
            header = response.get('header', {})
            event = header.get('event')

            if event == 'result-generated':
                output = response.get('payload')['output']
                if output.get('transcription', None) and output['transcription']['sentence_end']:
                    text += output['transcription']['text']
            elif event in ['task-finished', 'task-failed']:
                if header.get('error_message', None) is not None:
                    logger.error(header.get('error_message'))
                break
        return text

    async def run_asr_tasks(self, pcm_data: bytes) -> str | None:
        task_id = uuid.uuid4().hex
        api_key = os.getenv('ALIYUN_API_KEY') # DNE
        wss_url = os.getenv('ALIYUN_WSS_URL')

        headers = {"Authorization" : f"Bearer {api_key}"}

        async with websockets.connect(uri=wss_url, additional_headers=headers) as ws:
            await ws.send(json.dumps({
                "header": {
                    "streaming": "duplex",
                    "task_id": task_id,
                    "action": "run-task"
                },
                "payload": {
                    "model": "gummy-realtime-v1",
                    "parameters": {
                        "sample_rate": 16000,
                        "format": "pcm",
                        "transcription_enabled": True,
                    },
                    "input": {},
                    "task": "asr",
                    "task_group": "audio",
                    "function": "recognition"
                }
            }))

            async for msg in ws:
                # Ensure we are parsing a string message
                if isinstance(msg, bytes):
                    msg = msg.decode('utf-8')
                response = json.loads(msg)
                header = response.get('header', {})
                if header.get('event') == 'task-started':
                    break
            
            _, text = await asyncio.gather(
                self.asr_sender(pcm_data, ws, task_id),
                self.asr_receiver(ws)
            )
            return text