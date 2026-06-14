from django.utils.timezone import now
import logging

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.character import Character

from web.views.utils.profile_image import remove_old_image

logger = logging.getLogger(__name__)

class UpdateCharacterView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Request):
        try:
            character_id = request.data['character_id']
            character: Character = Character.objects.get(id=character_id, author__user=request.user)

            name = request.data['name'].strip()
            desc = request.data['desc'].strip()
            image = request.FILES.get('image', None)
            bg_image = request.FILES.get('bg_image', None)

            if not name:
                return Response({
                    'result' : '名字不能为空'
                })
            if not desc:
                return Response({
                    'result' : '角色介绍不能为空'
                })
        
            if image:
                remove_old_image(character.image)
                character.image = image
            if bg_image:
                remove_old_image(character.bg_image)
                character.bg_image = bg_image

            character.name = name
            character.desc = desc
            character.updated_at = now()
            character.save()

            return Response({
                'result' : 'success'
            }, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({ 'result' : '系统异常，请稍后重试'}, status=500)