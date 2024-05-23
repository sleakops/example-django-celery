from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "date_joined",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "groups",
    )
    search_fields = ["email", "last_name", "first_name",]
    ordering = ("email",)

    