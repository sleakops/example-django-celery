from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.http import urlencode
from apps.base.admin import related_link
from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "date_joined",
        "related_links",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "groups",
    )
    search_fields = ["email", "last_name", "first_name",]
    ordering = ("email",)

    def related_links(self, obj):
        query_param = urlencode({"user": f"{obj.id}"})
        return related_link(f"/admin/order/order/?{query_param}", "Orders") + related_link(f"/admin/cart/cart/?{query_param}", "Carts")