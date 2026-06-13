from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    plan = models.CharField(
        max_length=50
    )

    active = models.BooleanField(
        default=True
    )

    start_date = models.DateTimeField(
        auto_now_add=True
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True
    )