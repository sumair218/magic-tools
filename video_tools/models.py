from django.db import models
from django.contrib.auth.models import User

class DownloadHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    platform = models.CharField(
        max_length=50
    )

    url = models.URLField()

    downloaded_file = models.FileField(
        upload_to='downloads/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )