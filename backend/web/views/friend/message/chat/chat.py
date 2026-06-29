from django.http import StreamingHttpResponse

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import BaseRenderer
from rest_framework.permissions import IsAuthenticated

from langchain_core.messages import HumanMessage, BaseMessage

from web.models.friend import Friend
from web.views.friend.message.chat.graph import ChatGraph

import json
import logging
logger = logging.getLogger(__name__)


class SSERenderer(BaseRenderer):
    media_type = "text/event-stream"
    format = "txt"
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

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

            def event_stream():
                full_usage = {}
                for msg, metadata in app.stream(inputs, stream_mode="messages"):
                    if isinstance(msg, BaseMessage):
                        if msg.content:
                            yield f"data: {json.dumps({"content" : msg.content}, ensure_ascii=False)}\n\n"
                        if hasattr(msg, "usage_metadata") and msg.usage_metadata:
                            full_usage = msg.usage_metadata
                yield "data: [DONE]\n\n"
                print(full_usage)
            
            response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
            response['Cache-control'] = "no-cache"
            return response
        except Exception as e:
            logger.exception(e)
            return Response({ 'result' : '系统异常，请稍后重试' }, status=500)
