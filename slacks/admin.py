from django.contrib import admin

from slacks.models import Team


class TeamAdmin(admin.ModelAdmin):

    model = Team

    exclude = (
        'bot_access_token',
    )


admin.site.register(Team, TeamAdmin)
