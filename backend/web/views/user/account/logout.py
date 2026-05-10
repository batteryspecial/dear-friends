from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Implement your logout flow here

class LogoutView(APIView):
    permission_classes = [IsAuthenticated] # enforce login state, otherwise 401 unauthorized
    
    def post(self, request):
        response = Response({
            'result' : 'success',
        })

        response.delete_cookie('refresh_token') # will not throw if token dne
        return response
