from .models import Order, OrderItem
from django.contrib import admin, messages
# from django.utils.http import urlencode

# from apps.base.admin import related_link
# from apps.client.models import Client
from apps.order.tasks import order_process


@admin.action(description="Run collect post task")
def process_orders(modeladmin, request, queryset):
    # loop each client and dispatch task to collect post
    for o in queryset.all():
        order_process.delay(o.id)
    messages.add_message(
        request,
        messages.INFO,
        f"Todas las ordenes seleccionadas fueron enviadas para su procesamiento",
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    actions = [process_orders]
    # list_display = ("id", "source", "client", "created_at")
    # search_fields = ("client_id",)
    # list_filter = (
    #     "source",
    #     "client",
    # )
    # def related_links(self, obj):
    #     query_param = urlencode({"client_id": f"{obj.id}"})
    #     return related_link(f"/admin/post/post/?{query_param}", "Posts")

admin.site.register(OrderItem)
