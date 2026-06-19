from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.character import Character
from web.views.utils.profile_image import remove_old_image


class DeleteCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        try:
            character_id = request.data['character_id']
            character = Character.objects.get(pk=character_id, author__user=request.user)

            remove_old_image(character.image)
            remove_old_image(character.bg_image)

            character.delete()

            return Response({
                'result' : 'success',
            }, status=200)
        except:
            return Response({
                'result' : '系统异常，请稍后重试'
            }, status=500)
