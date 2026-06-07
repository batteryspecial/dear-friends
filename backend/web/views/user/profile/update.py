from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.user import UserProfile
from web.views.utils.profile_image import remove_old_image
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils.timezone import now

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Request):
        try:
            user: User = request.user
            user_profile = get_object_or_404(UserProfile, user=request.user)

            new_username = request.data.get("username").strip()
            new_bio = request.data.get("bio").strip()[:500]
            # use the image only when we need it
            new_image = request.FILES.get("image", None)

            if not new_username:
                return Response({
                    'result' : '用户名不能为空'
                }, status=400)
            
            if not new_bio:
                return Response({
                    'result' : '简介不能为空'
                }, status=400)
            
            if (new_username != user.username and User.objects.filter(username=new_username).exists()):
                return Response({
                    'result' : '用户名已被占用'
                }, status=400)
            
            if new_image:
                remove_old_image(image=user_profile.image)
                user_profile.image = new_image

            user_profile.bio = new_bio
            user_profile.updated_at = now()
            user_profile.save()

            user.username = new_username
            user.save()

            return Response({
                'result' : 'success',
                'user_id' : user.id,
                'username' : user.username,
                'bio' : user_profile.bio,
                'image' : user_profile.image.url,
            }, status=200)
        except:
            return Response({
                'result' : '系统异常，请稍后重试'
            }, status=500)
