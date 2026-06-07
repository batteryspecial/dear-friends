import uuid

from django.contrib.auth.models import User
from django.utils.timezone import now, localtime
from django.db import models

def img_upload_to(instance, filename):
    ext = filename.split()[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'

    return f'user/img/{instance.user_id}_{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='user/img/default.png', upload_to=img_upload_to) # requires Pillow
    bio = models.TextField(default='感谢同志们的关注', max_length=500)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.user.username} | {localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S')}'