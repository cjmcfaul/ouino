import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    '''
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
    '''