import uuid

from django.db import models


# Create your models here.
class Question(models.Model):

    public_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    created_by = models.CharField(
        max_length=100,
    )
    question_text = models.CharField(
        max_length=140,
    )
    channel_id = models.CharField(
        max_length=100,
    )
