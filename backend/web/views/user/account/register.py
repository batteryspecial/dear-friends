from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from web.models.user import UserProfile

# Implement your registration flow here

class RegisterView(APIView):
    def post(self, request: Request):
        try:
            username = request.data.get('username').strip()
            password = request.data.get('password').strip()

            if not username or not password:
                return Response({
                    'result' : '用户名和密码不能为空'
                })
            
            if User.objects.filter(username=username).exists():
                return Response({
                    'result' : '用户名已存在，请重试'
                })
            
            user = User.objects.create_user(username=username, password=password)
            user_profile = UserProfile.objects.create(user=user)

            # token time
            refresh = RefreshToken.for_user(user)

            response = Response({
                'result' : 'success',
                'access' : str(refresh.access_token),
                'user_id' : user.id,
                'username' : user.username,
                'image' : user_profile.image.url,
                'profile' : user_profile.bio,
            })

            response.set_cookie(
                key='refresh_token', 
                refresh=str(refresh), 
                httponly=True, 
                samesite='Lax', 
                secure=True,
                max_age=86400 * 6.7
            )

            return response
        except:
            return Response({
                'result' : '系统异常，请稍后重试'
            })
