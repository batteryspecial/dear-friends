from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Friend

import logging
mogger = logging.getLogger(__name__)

class RemoveFriendView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Request):
        try:
            friend_id = request.data["friend_id"]
            Friend.objects.filter(id=friend_id, me__user=request.user).delete()

            return Response({ 'result' : 'success' }, status=200)
        except Exception as e:
            mogger.exception(e)
            return Response({ 'result' : '系统异常，请稍后重试' }, status=500)