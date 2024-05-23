from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import path, include


def healthcheck(request):
    """
        View to configure healthcheck for the project
    """
    return HttpResponse("ok")


urlpatterns = [
    path("healthcheck/", healthcheck),
    path('admin/', admin.site.urls),
]


# Static file serving when using Gunicorn + Uvicorn for local web socket development
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))] + urlpatterns