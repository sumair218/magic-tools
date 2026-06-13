from django.db import models
from django.contrib.auth.models import User

class PDFHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    tool_name = models.CharField(
        max_length=100
    )

    input_file = models.FileField(
        upload_to='pdf/input/'
    )

    output_file = models.FileField(
        upload_to='pdf/output/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.tool_name