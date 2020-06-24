"""yes_no URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from users.views import (
    support,
    install,
    feedback,
    more_info
)

urlpatterns = [
    path(
        'api/',
        include('yes_no.api_urls')
    ),
    path('slack/', include('slacks.urls')),
    path('admin/', admin.site.urls),
    path(
        'feedback/',
        feedback,
        name='feedback'
    ),
    path(
        'support/',
        support,
        name='support'
    ),
    path(
        'install/',
        install,
        name='install'
    ),
    path(
        'terms-and-conditions/',
        TemplateView.as_view(template_name='info-pages/terms_and_conditions.html'),
        name='terms_and_conditions'
    ),
    path(
        'privacy-policy/',
        TemplateView.as_view(template_name='info-pages/privacy_policy.html'),
        name='privacy_policy'
    ),
    path(
        'more-info/',
        more_info,
        name='more_info'
    ),
    path(
        '',
        TemplateView.as_view(template_name='home.html'),
        name='home'
    )
]
