from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Friend

import logging
mogger = logging.getLogger(__name__)

class GetFriendListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        try:
            items_count = int(request.query_params.get("items_count", 0))
            friends_raw = Friend.objects.filter(me__user=request.user).order_by("-updated_at")[items_count : items_count + 20]

            friends = []
            for f in friends_raw:
                character = f.character
                author = character.author
                friends.append({
                    "id" : f.id,
                    "character" : {
                        "id" : character.id,
                        "name" : character.name,
                        "desc" : character.desc,
                        "image" : character.image.url,
                        "bg_image" : character.bg_image.url,
                        "author" : {
                            "user_id" : author.id,
                            "username" : author.user.username,
                            "image" : author.image.url,
                        }
                    }
                })
            
            return Response({ 'result' : 'success', 'friends' : friends }, status=200)
        except Exception as e:
            mogger.exception(e)
            return Response({ 'result' : '系统异常，请稍后重试' }, status=500)