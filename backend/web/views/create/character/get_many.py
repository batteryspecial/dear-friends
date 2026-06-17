from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from django.contrib.auth.models import User
from web.models.user import UserProfile
from web.models.character import Character

import logging

logger = logging.getLogger(__name__)

class GetCharacterListView(APIView):
    def get(self, request: Request):
        try:
            items_count = int(request.query_params.get('items_count'))
            user_id = request.query_params.get('user_id')
            user = User.objects.get(id=user_id)
            user_profile = UserProfile.objects.get(user=user)

            characters_raw = Character.objects.filter(author=user_profile).order_by('-id')[items_count : items_count + 20]
            
            characters = []
            for c in characters_raw:
                author = c.author
                characters.append({
                    'id' : c.id,
                    'name' : c.name,
                    'desc' : c.desc,
                    'image' : c.image.url,
                    'bg_image' : c.bg_image.url,
                    'author' : {
                        'user_id' : author.user_id,
                        'username' : author.user.username,
                        'image' : author.image.url,
                    }
                })
            
            return Response({
                'result' : 'success',
                'user_profile' : {
                    'user_id' : user.id,
                    'username' : user.username,
                    'bio' : user_profile.bio,
                    'image' : user_profile.image.url,
                },
                'characters' : characters,
            }, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({ 'result' : '系统异常，请稍后重试' }, status=500)

