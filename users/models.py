import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    slack_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    slack_username = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    slack_access_token = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    team = models.ForeignKey(
        'slacks.Team',
        blank=True,
        null=True,
        related_name='members',
        on_delete=models.CASCADE
    )
    onboarding_complete = models.BooleanField(
        default=False
    )
