from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User

class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "role", "is_active")
    ordering = ("-date_joined",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()