from django.utils.html import format_html


from django.contrib import admin

admin.site.site_header = "Backoffice Administration"
admin.site.site_title = "Backoffice Administration"
admin.site.index_title = "Welcome to Backoffice Administration"


def related_link(url, name):
    return format_html(
        '<a class="related_link" href="{}">{} <span class="tooltiptext">{}</span></a>',
        url,
        name,
        name,
    )