from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.character import Character

class GetCharacterView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request):
        try:
            character_id = request.query_params.get('character_id')
            character = Character.objects.get(id=character_id, author__user=request.user)

            return Response({
                'result' : 'success',
                'character' : {
                    'id' : character_id,
                    'name' : character.name,
                    'desc' : character.desc,
                    'image' : character.image.url,
                    'bg_image' : character.bg_image.url,
                }
            }, status=200)
        except:
            return Response({
                'result' : '系统异常，请稍后重试'
            }, status=500)