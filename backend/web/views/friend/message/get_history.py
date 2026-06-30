from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Message

import logging
mogger = logging.getLogger(__name__)

class GetChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request):
        try:
            last_message_id = int(request.query_params.get('last_message_id'))
            friend_id = request.query_params.get('friend_id')
            queryset = Message.user_message.filter(friend_id=friend_id, friend__me__user=request.user)
            
            if (last_message_id > 0):
                queryset = queryset.filter(pk__lt=last_message_id)

            messages_raw = queryset.order_by('-id')[:10]
            messages = []
            for m in messages_raw:
                messages.append({
                    'id': m.id,
                    'user_message': m.user_message,
                    'output': m.output,
                })
            return Response({ 'result' : 'success', 'messages' : messages }, status=200)
        except Exception as e:
            mogger.exception(e)
            return Response({ 'result' : '系统异常，请稍后重试' }, status=500)