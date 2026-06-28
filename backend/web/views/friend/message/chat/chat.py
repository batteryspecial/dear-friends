from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from langchain_core.messages import HumanMessage

from web.models.friend import Friend
from web.views.friend.message.chat.graph import ChatGraph

import logging
logger = logging.getLogger(__name__)

class MesssageChatView(APIView):
    permission_classes = [IsAuthenticated]
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
            r = app.invoke(input=inputs)
            print(r["messages"][-1].content)
            return Response({ 'result' : 'success' }, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({ 'result' : '系统异常，请稍后重试' }, status=500)
