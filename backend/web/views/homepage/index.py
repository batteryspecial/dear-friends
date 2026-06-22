from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.models import Q
from web.models.character import Character

import logging
logger = logging.getLogger(__name__)

class HomepageIndexView(APIView):
    def get(self, request: Request):
        try:
            items_count = int(request.query_params.get('items_count', 0))
            search_query = request.query_params.get('search_query', '')
            if search_query:
                queryset = Character.objects.filter(Q(name__icontains=search_query) | Q(desc__icontains=search_query))
            else:
                queryset = Character.objects.all()

            characters_raw = queryset.order_by('-id')[items_count : items_count + 20]
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
                'characters' : characters,
            }, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({ 'result' : '系统异常，请稍后重试'}, status=500)
