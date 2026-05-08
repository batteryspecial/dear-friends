from django.urls import path, re_path
from . import views

# Create your urls here

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.home, name='homepage'),
    path('api/auth/get_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # re_path(r'^(?!media/|static/|assets/).*$'),
]
