from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.user import UserProfile
from web.models.friend import Friend

import logging
logger = logging.getLogger(__name__)


class GetOrCreateFriendView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Request):
        try:
            character_id = request.data["character_id"]
            user = request.user
            user_profile = UserProfile.objects.get(user=user)

            friends = Friend.objects.filter(character_id=character_id, me=user_profile)
            if friends.exists():
                friend = friends.first()
            else:
                friend = Friend.objects.create(me=user_profile, character_id=character_id)
            
            character = friend.character
            author = character.author

            return Response({
                "result" : "success",
                "friend" : {
                    "id" : friend.id,
                    "character" : {
                        "id" : character.id,
                        "name" : character.name,
                        "bio" : character.desc,
                        "image" : character.image.url,
                        "bg_image" : character.bg_image.url,
                        "author" : {
                            "user_id" : author.id,
                            "username" : author.user.username,
                            "image" : author.image.url,
                        }
                    }
                }
            })
        except Exception as e:
            logger.exception(e)
            return Response({ 'result' : '系统异常，请稍后重试' }, status=500)
