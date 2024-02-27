from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "role", "is_active")
    ordering = ("-date_joined",)
    filter_horizontal = ()
    list_filter = (
        "role",
        "is_active",
    )
    fieldsets = ()
    readonly_fields = [
        "email",
        "role",
    ]
