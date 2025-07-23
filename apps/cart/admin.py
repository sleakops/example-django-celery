from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    # list_display = ("id", "source", "client", "created_at")
    # search_fields = ("client_id",)
    # list_filter = (
    #     "source",
    #     "client",
    # )


admin.site.register(CartItem)
