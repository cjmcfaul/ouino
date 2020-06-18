from django.urls import path

from slacks import api_views as views


urlpatterns = [
    path(
        'interactive-commands/',
        views.interactive_commands
    ),
    path(
        'question/',
        views.question
    ),
    path(
        'events/',
        views.events
    )
]
