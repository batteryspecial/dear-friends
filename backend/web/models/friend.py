from django.db import models
from django.utils.timezone import now, localtime
from web.models.user import UserProfile
from web.models.character import Character

# Create your friend models here.

class Friend(models.Model):
    me = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    character = models.ForeignKey(to=Character, on_delete=models.CASCADE)
    memory = models.TextField(default="", max_length=5000, blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.character.name} | {self.me.user.username} |{localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S')}"