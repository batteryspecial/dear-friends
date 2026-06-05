from django.conf import settings

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

# Implement your access token refresh here
# - access lives in cache (frontend)
# - refresh lives in HTTP-only cookie (backend)

class RefreshTokenView(APIView):
    def post(self, request: Request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({
                    'result' : 'refresh token 不存在',
                }, status=401)
            
            refresh = RefreshToken(refresh_token) # if refresh_token is expired, will throw
            if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS'): 
                refresh.set_jti()
                response = Response({
                    'result' : 'success',
                    'access' : str(refresh.access_token)
                }, status=200)
                response.set_cookie(
                    key='refresh_token', 
                    value=str(refresh), 
                    httponly=True, 
                    samesite='Lax',
                    secure=True,
                    max_age=86400 * 6.7
                )
                return response
            return Response({
                'result' : 'success',
                'access' : str(refresh.access_token)
            }, status=200)
        except:
            return Response({
                'result' : 'refresh token 过期了',
            }, status=401)
