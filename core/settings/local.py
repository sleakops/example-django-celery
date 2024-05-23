import mimetypes
from datetime import timedelta

from .base import *  # noqa
from .base import env

ENVIRONMENT = "local"


# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": "",
#     }
# }

# django-debug-toolbar & django-silk
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/
INSTALLED_APPS += ["debug_toolbar",]  # noqa F405

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware"
] + MIDDLEWARE  # noqa F405


DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda x: True, "RENDER_PANELS": True}

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "0.0.0.0", "localhost"]

# EMAILS CONFIG
# ------------------------------------------------------------------------------

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


TASKS_DEFAULT_CANVAS_COUNTDOWN = 5
TASKS_DEFAULT_MODULES_COUNTDOWN = 5
TASKS_DEFAULT_MAX_RETRIES = 100
