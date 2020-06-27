from django.dispatch import receiver
from django.db.models.signals import post_save

from slacks.models import Team

from slacks.tasks import new_team_create_users


@receiver(post_save, sender=Team)
def create_team_users(instance, created):
    if created:
        new_team_create_users.apply_async([instance.public_id, ])
