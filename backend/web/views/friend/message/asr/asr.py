import threading

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import numpy

import logging
logger = logging.getLogger(__name__)


MLX_MODEL_REPO = "mlx-community/whisper-tiny"   # Apple Silicon (Metal)
FW_MODEL = "tiny"                               # Linux/CPU (CTranslate2)

# Inference is not thread-safe under Django's threaded server, and the Linux box
# is a 2-vCPU t3.micro anyway. One at a time; move to a worker queue if
# concurrent speakers ever matter (they don't).
_inference_lock = threading.Lock()
_transcribe = None  # built on first request: model load is slow, don't pay it at import


# Tuned for a 2-vCPU t3.micro, not accuracy: greedy decoding instead of a
# 5-beam search, VAD to skip silence (and Whisper's hallucinations over it),
# and no cross-request context since each POST is an independent utterance.
FW_OPTIONS = {
    'beam_size': 1,
    'vad_filter': True,
    'condition_on_previous_text': False,
    'without_timestamps': True,
}


def _build_transcriber():
    """Pick the ASR backend this machine can actually run.

    mlx-whisper is Apple-Silicon-only (it imports the `mlx` Metal runtime).
    faster-whisper is CTranslate2 and runs anywhere, so it is the Linux path.
    Both take a 16kHz mono float32 array and return text.
    """
    # ImportError, not ModuleNotFoundError: a leftover pip install of mlx-whisper
    # on Linux imports fine until it dlopens libmlx.so, which only exists on macOS.
    try:
        import mlx_whisper
    except ImportError:
        from faster_whisper import WhisperModel

        model = WhisperModel(FW_MODEL, device='cpu', compute_type='int8')
        logger.info('ASR backend: faster-whisper (%s, int8 CPU)', FW_MODEL)

        def run(audio_data):
            # faster-whisper streams lazily; the generator only runs on iteration.
            segments, _ = model.transcribe(audio_data, language='zh', **FW_OPTIONS)
            return ''.join(segment.text for segment in segments)
    else:
        logger.info('ASR backend: mlx-whisper (%s)', MLX_MODEL_REPO)

        def run(audio_data):
            return mlx_whisper.transcribe(
                audio=audio_data, path_or_hf_repo=MLX_MODEL_REPO, language='zh'
            ).get('text', '')

    return run


class ASRView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        global _transcribe

        audio = request.FILES.get('audio')
        if not audio:
            return Response({ 'result' : '音频不存在' }, status=400)

        pcm_data = audio.read()
        if (len(pcm_data) < 2) or (len(pcm_data) % 2 != 0):
            return Response({'result': '音频格式错误'}, status=400)

        # frontend float32ToInt16 produces 16kHz mono PCM16 -> back to float32
        audio_data = numpy.frombuffer(pcm_data, dtype=numpy.int16).astype(numpy.float32) / 32768.0

        try:
            # Lock covers the load too, so two first-requests can't both build a model.
            with _inference_lock:
                if _transcribe is None:
                    _transcribe = _build_transcriber()
                text = _transcribe(audio_data).strip()
        except Exception:
            logger.exception('ASR 推理失败')
            return Response({'result': '语音识别失败'}, status=500)

        if not text:
            return Response({'result': '未识别到语音'}, status=200)

        return Response({'result' : 'success', 'text' : text }, status=200)
