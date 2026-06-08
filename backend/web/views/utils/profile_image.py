from django.core.files.uploadedfile import UploadedFile
from typing import Any

from django.conf import settings
import os

# Implement your profile image utils here

def remove_old_image(image: UploadedFile | Any) -> None:
    if (image and image.name != 'user/img/default.png'):
        old_path = settings.MEDIA_ROOT / image.name
        if os.path.exists(old_path):
            os.remove(old_path)
    

