import uuid

from django.db import models


class Team(models.Model):
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    slack_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
