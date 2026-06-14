from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.user import UserProfile
from web.models.character import Character

import logging as mogging

mogger = mogging.getLogger(__name__)

class CreateCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            name = request.data.get("name", "").strip()
            desc = request.data.get("desc", "").strip()[:6767]
            image = request.FILES.get("image", None)
            bg_image = request.FILES.get("bg_image", None)

            if not name:
                return Response({ 'result' : '名字不能为空' }, status=400)
            if not desc:
                return Response({ 'result' : '角色介绍不能为空' }, status=400)
            if not image:
                return Response({ 'result' : '头像不能为空' }, status=400)
            
            character_data = {
                'author' : user_profile,
                'name' : name,
                'desc' : desc,
                'image' : image,
            }
            if bg_image:
                character_data['bg_image'] = bg_image
            
            Character.objects.create(**character_data)
            return Response({ 'result' : 'success' }, status=200)
        except Exception as e:
            mogger.exception(e)
            return Response({ 'result' : '系统异常，请稍后重试' }, status=500)
