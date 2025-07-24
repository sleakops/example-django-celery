from os.path import join
from pathlib import Path
import environ

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# core/
APPS_DIR = ROOT_DIR / "apps"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)

ENVIRONMENT = env("ENVIRONMENT")

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["*"])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "crispy_forms",
    "crispy_bootstrap5",
    "apps.base",
    "apps.user",
    # "apps.client",
    # "apps.post",
    "apps.product",
    "apps.cart",
    "apps.order",
    "apps.payment",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
         # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [f"{ROOT_DIR}/core/templates/"],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'apps.cart.context_processors.cart_count',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": env.str("DB_ENGINE", "django.db.backends.postgresql_psycopg2"),
        "NAME": env.str("DB_NAME", 'dbexample'),
        "USER": env.str("DB_USER", "user"),
        "PASSWORD": env.str("DB_PASSWORD", "password"),
        "HOST": env.str("DB_HOST", "localhost"),
        "PORT": env.str("DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = "user.User"


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

CELERY_ENABLED = env.bool("DJANGO_CELERY_ENABLED", default=False)

if CELERY_ENABLED:
    INSTALLED_APPS += ["django_celery_results"]
    # Celery
    CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", default="django-db")
    CELERY_WORKER_PREFETCH_MULTIPLIER = env.int(
        "CELERY_WORKER_PREFETCH_MULTIPLIER", default=1
    )
    CELERY_RESULT_EXTENDED = env.bool("CELERY_RESULT_EXTENDED", default=False)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = f"{ROOT_DIR}/static"

STATICFILES_DIRS = [f"{ROOT_DIR}/core/static/"]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = "login"                 # nombre del path
LOGIN_REDIRECT_URL = "home"         # adónde después de login
LOGOUT_REDIRECT_URL = "home"        # adónde después de logout


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


LOAD_STATIC_AND_MEDIA=env.bool("DJANGO_LOAD_STATIC_AND_MEDIA", default=True)


ADMIN_ENABLED = env.bool("ADMIN_ENABLED", default=True)