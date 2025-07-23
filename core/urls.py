from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import path, include
from django.views.generic import TemplateView
from apps.product.models import Product


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        return {
            "products": Product.objects.order_by('?')[:4]
        }


def healthcheck(request):
    """
        View to configure healthcheck for the project
    """
    return HttpResponse("ok")


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("healthcheck/", healthcheck),
    path("", include("apps.user.urls")),
    path("", include("apps.cart.urls")),
    path("", include("apps.order.urls")),
    path("", include("apps.product.urls")),
]

# Admin URL configuration
if settings.ADMIN_ENABLED:
    urlpatterns += [
        path("admin/", admin.site.urls),
    ]


# Static file serving when using Gunicorn + Uvicorn for local web socket development
if settings.LOAD_STATIC_AND_MEDIA:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))] + urlpatterns