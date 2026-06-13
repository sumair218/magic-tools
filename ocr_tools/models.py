from django.db import models
from django.contrib.auth.models import User

class OCRHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    file = models.FileField(
        upload_to='ocr/'
    )

    extracted_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )