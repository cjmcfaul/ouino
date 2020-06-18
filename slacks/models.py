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
    bot_access_token = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    bot_slack_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
