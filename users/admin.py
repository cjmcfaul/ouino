from django.contrib import admin

from users.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):

    model = CustomUser

    exclude = (
        'slack_access_token',
    )


admin.site.register(CustomUser, CustomUserAdmin)
