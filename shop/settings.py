import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DOMAIN = "http://127.0.0.1:8000"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-1l=q+we=ui-&g-b+$7^c6d&yy1@^&@updg24n@wh44j+0wd603"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "store",
    "customer",
    "phonenumber_field",
    "django_filters",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "store.middleware.OrderMiddleware",
]

ROOT_URLCONF = "shop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "shop.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/images/'

MEDIA_ROOT = os.path.join(BASE_DIR / 'static/images')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Stripe secrets
STRIPE_SECRET_KEY = "sk_test_51LWJgoF2YQvlQ4aeDIMxc53WGCSDucnLbUv3f3tdmohpQGpCoD5JnbVR0tiP8NyXRXoevLfVLD5xULHjWeU0GRs6004Pkyq9M5"
STRIPE_PUBLIC_KEY = "pk_test_51LWJgoF2YQvlQ4aeBfK1PNJxdPmpgsxqbuBqpFzFqo8HElKG7RUK1MqvSfD3MVWNRUghG1GO3Saq2pPVHN1v4gsQ00ZhEAMrNE"
STRIPE_WEBHOOK_SECRET = "whsec_c6ccb3b147b5bc7fc67765fd53f1b7058792c703595ee3bd0badee5fc8d94e34"

AUTH_USER_MODEL = 'customer.Customer'
