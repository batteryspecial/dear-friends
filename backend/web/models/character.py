import uuid
from django.db import models
from django.utils.timezone import now, localtime

from web.models.user import UserProfile

def img_upload_to(instance, filename):
    ext = filename.split()[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    return f'character/img/{instance.author.user_id}_{filename}'

def bg_upload_to(instance, filename):
    ext = filename.split()[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    return f'character/bg/{instance.author.user_id}_{filename}'

class Character(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=67)
    image = models.ImageField(upload_to=img_upload_to)
    desc = models.TextField(max_length=6767)
    bg_image = models.ImageField(upload_to=bg_upload_to)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.author.user.username} | {self.name} |{localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S')}"
