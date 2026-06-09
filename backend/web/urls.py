from django.urls import path, re_path
from . import views

# Create your urls here

from web.views.user.account.login import LoginView
from web.views.user.account.logout import LogoutView
from web.views.user.account.register import RegisterView
from web.views.user.account.refresh_token import RefreshTokenView
from web.views.user.account.get_user_info import GetUserInfoView
from web.views.user.profile.update import UpdateProfileView

from web.views.create.character.create import CreateCharacterView
from web.views.create.character.update import UpdateCharacterView
from web.views.create.character.delete import DeleteCharacterView
from web.views.create.character.get_ch import GetCharacterView

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
    path('api/user/profile/update/', UpdateProfileView.as_view(), name='update_profile_view'),

    path('api/create/character/create/', CreateCharacterView.as_view(), name='create_character_view'),
    path('api/create/character/update/', UpdateCharacterView.as_view(), name='update_character_view'),
    path('api/create/character/delete/', DeleteCharacterView.as_view(), name='delete_character_view'),
    path('api/create/character/get_ch/', GetCharacterView.as_view(), name='get_character_view'),

    path('', views.home, name='homepage'),
    re_path(r'^(?!media/|static/|assets/).*$', views.home),
]
