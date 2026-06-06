from django.urls import path, re_path
from . import views

# Create your urls here

from web.views.user.account.login import LoginView
from web.views.user.account.logout import LogoutView
from web.views.user.account.register import RegisterView
from web.views.user.account.refresh_token import RefreshTokenView

from web.views.user.account.get_user_info import GetUserInfoView

"""
- If frontend and backend urls match -> TemplateNotExist
- Django will try loading using its own urls first
- This is why we add 'api/' before backend urls
"""

urlpatterns = [
    path('api/user/account/login/', LoginView.as_view(), name='login_view'),
    path('api/user/account/logout/', LogoutView.as_view(), name='logout_view'),
    path('api/user/account/register/', RegisterView.as_view(), name='register_view'),
    path('api/user/account/refresh_token/', RefreshTokenView.as_view(), name='refresh_token_view'),
    path('api/user/account/get_user_info/', GetUserInfoView.as_view(), name='get_user_info_view'),
    
    path('', views.home, name='homepage'),
    re_path(r'^(?!media/|static/|assets/).*$', views.home),
]
