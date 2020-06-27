from __future__ import absolute_import, unicode_literals

from yes_no.celery import app

from slacks.models import Team
from slacks.backends import create_users_from_team


@app.task
def new_team_create_users(team_id):
    team = Team.objects.get(public_id=team_id)
    create_users_from_team(team)
