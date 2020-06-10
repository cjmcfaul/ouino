from django.urls import path, include

urlpatterns = [
    path(
        'slack/',
        include('slacks.api_urls')
    ),
]
