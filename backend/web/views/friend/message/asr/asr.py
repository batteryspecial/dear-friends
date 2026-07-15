from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import numpy
import threading
import mlx_whisper

import logging
logger = logging.getLogger(__name__)


MODEL_REPO = "mlx-community/whisper-tiny"
# MLX inference is not thread-safe under Django's threaded server.
# One GIL, move to a worker queue if concurrent speakers matter (it doesn't).
_inference_lock = threading.Lock()

class ASRView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        audio = request.FILES.get('audio')
        if not audio:
            return Response({ 'result' : '音频不存在' }, status=400)

        pcm_data = audio.read()
        if (len(pcm_data) < 2) or (len(pcm_data) % 2 != 0):
            return Response({'result': '音频格式错误'}, status=400)
        
        # frontend float32ToInt16 produces 16kHz mono PCM16 -> back to float32
        audio_data = numpy.frombuffer(pcm_data, dtype=numpy.int16).astype(numpy.float32) / 32768.0

        try:
            with _inference_lock:
                result = mlx_whisper.transcribe(audio=audio_data, path_or_hf_repo=MODEL_REPO, language='zh')
        except Exception:
            logger.exception('ASR 推理失败')
            return Response({'result': '语音识别失败'}, status=500)
        
        text = result.get('text', '').strip()
        if not text:
            return Response({'result': '未识别到语音'}, status=200)

        return Response({'result' : 'success', 'text' : text }, status=200)

