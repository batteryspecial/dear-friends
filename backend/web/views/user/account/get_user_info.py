from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated

from web.models.user import UserProfile


class GetUserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)

            return Response({
                'result' : 'success',
                'user_id' : user.id,
                'username' : user.username,
                'image' : user_profile.image.url,
                'bio' : user_profile.bio,
            }, status=200)
        except:
            return Response({
                'result' : '系统异常，请稍后重试'
            }, status=500)

