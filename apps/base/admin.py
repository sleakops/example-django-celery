from django.utils.html import format_html


def related_link(url, name):
    return format_html(
        '<a class="related_link" href="{}">{} <span class="tooltiptext">{}</span></a>',
        url,
        name,
        name,
    )