from django.db import models
from django.contrib.auth.models import User

class ImageHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='images/'
    )

    tool_used = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )