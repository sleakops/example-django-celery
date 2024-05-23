from django.contrib import admin, messages
from django.utils.http import urlencode

from apps.base.admin import related_link
from apps.client.models import Client
from apps.client.tasks import collect_post_by_client



@admin.action(description="Run collect post task")
def collect_post(modeladmin, request, queryset):
    # loop each client and dispatch task to collect post
    for c in queryset.all():
        collect_post_by_client.delay(c.id)
        messages.add_message(
            request,
            messages.INFO,
            f"Run collect post task for client {c.username}",
        )


@admin.register(Client)
class AdminClient(admin.ModelAdmin):
    list_display = ("id","username", "created_at", "related_links")
    search_fields = ("username", "full_name")
    actions = [collect_post] # https://docs.djangoproject.com/en/5.0/ref/contrib/admin/actions/#adding-actions-to-the-modeladmin

    def related_links(self, obj):
        query_param = urlencode({"client_id": f"{obj.id}"})
        return related_link(f"/admin/post/post/?{query_param}", "Posts")
