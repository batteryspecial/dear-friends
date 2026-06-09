from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.user import UserProfile
from web.models.character import Character

class CreateCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            name = request.get("name").strip()
            desc = request.get("desc").strip()[:6767]
            image = request.FILES.get("image", None)
            bg_image = request.FILES.get("bg_image", None)

            if not name:
                return Response({
                    'result' : '名字不能为空'
                })
            if not desc:
                return Response({
                    'result' : '角色介绍不能为空'
                })
            if not image:
                return Response({
                    'result' : '头像不能为空'
                })
            if not bg_image:
                return Response({
                    'result' : '聊天背景不能为空'
                })
            
            Character.objects.create(
                author=user_profile,
                name=name,
                desc=desc,
                image=image,
                bg_image=bg_image if bg_image else None,
            )
            return Response({
                'result' : 'success'
            }, status=200)
        except:
            return Response({
                'result' : '系统异常，请稍后重试'
            }, status=500)
