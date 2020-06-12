import uuid

from django.db import models


# Create your models here.
class Question(models.Model):

    CHOICES = (
        ('U', 'Urgent'),
        ('N', 'Normal'),
        ('W', 'Whenever')
    )

    public_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    created_by = models.CharField(
        max_length=100,
    )
    status = models.CharField(
        choices=CHOICES,
        max_length=2,
        blank=True,
        null=True
    )
    question_text = models.CharField(
        max_length=140,
    )
    channel_id = models.CharField(
        max_length=100,
    )
    message_ts = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
