from django.contrib import admin

from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ("id", "source", "client", "created_at")
    search_fields = ("client_id",)
    list_filter = (
        "source",
        "client",
    )


admin.site.register(Comment)
# admin.site.register(Post)
