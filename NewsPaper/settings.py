"""
Django settings for NewsPaper protect.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
import logging

from django.core.mail import send_mail

# Build paths inside the protect like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-_v$&c)&1a2soq8*z#q20lm6_f$qfi*rshu$^9mgqm8%iwdfm8*"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django_filters",
    "News_Portal",
    "simpleapp",
    "sign",
    "django_apscheduler",
    "celery",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "NewsPaper.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "NewsPaper.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATICFILES_DIRS = [BASE_DIR / "static"]

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/news/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_FORMS = {"signup": "sign.models.BasicSignupForm"}

EMAIL_HOST = "smtp.yandex.ru"
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_PORT = 465
EMAIL_HOST_USER = "pol9.f"
EMAIL_HOST_PASSWORD = "#*QXT0F5$s2$"
EMAIL_USE_SSL = True
ADMINS = [
    ("twonky", "pol9.f@yandex.ru"),
]
SERVER_EMAIL = "pol9.f@yandex.ru"

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

USE_L10N = True

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Europe/Amsterdam"

CACHES = {
    "default": {
        "TIMEOUT": 60,  # добавляем стандартное время ожидания в минуту (по умолчанию это 5 минут — 300 секунд)
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "cache_files"),
    }
}

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

# =============
class MyEmailHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET, email=None):
        if email is None:
            raise ValueError("Email should be set!")

        self.destination_email = email
        super().__init__(level)

    def emit(self, record) -> None:
        send_mail(
            f"Log record: {record.levelname}",
            self.format(record),
            SERVER_EMAIL,
            ("Log Receiver", self.destination_email),
        )


class NoExceptionInfoFormatter(logging.Formatter):
    def formatMessage(self, record) -> str:
        record.exc_info = None
        record.exc_text = None
        return super().formatMessage(record)


def filter_maker(level):
    level = getattr(logging, level)

    def filter(record):
        return record.levelno <= level

    return filter


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "debug_fmt": {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
        },
        "warning_fmt": {
            "format": "%(asctime)s - %(levelname)s - %(pathname)s - %(message)s",
        },
        "module_fmt": {
            "format": "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
        },
        "no_stack_trace_fmt": {
            "format": "%(asctime)s - %(levelname)s - %(module)s - %(message)s",
            "()": "NewsPaper.settings.NoExceptionInfoFormatter",
        },
    },
    "filters": {
        "debug_msg_only": {"level": "DEBUG", "()": "NewsPaper.settings.filter_maker"},
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console_debug": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "debug_fmt",
            "filters": ["debug_msg_only", "require_debug_true"],
        },
        "console_warning": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "warning_fmt",
            "filters": ["require_debug_true"],
        },
        "general_log": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "general.log",
            "formatter": "no_stack_trace_fmt",
            "filters": ["require_debug_false"],
        },
        "errors_log": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "errors.log",
            "formatter": "module_fmt",
        },
        "security_log": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "security.log",
            "formatter": "module_fmt",
        },
        "mail_admins": {
            "level": "DEBUG",
            "class": "NewsPaper.settings.MyEmailHandler",
            "email": "pol9@list.ru",
            "formatter": "no_stack_trace_fmt",
        },
    },
    "loggers": {
        "django": {
            "handlers": [
                "console_debug",
                "console_warning",
                "general_log",
            ],
            "propagate": False,
            "level": "DEBUG",
        },
        "django.request": {
            "handlers": [
                "mail_admins",
                "errors_log",
            ],
            "level": "ERROR",
        },
        "django.server": {
            "handlers": [
                "errors_log",
                "mail_admins",
            ],
            "level": "ERROR",
        },
        "django.template": {
            "handlers": [
                "errors_log",
            ],
            "level": "ERROR",
        },
        "django.db.backends": {
            "handlers": [
                "errors_log",
            ],
            "level": "ERROR",
        },
        "django.security": {
            "handlers": [
                "security_log",
            ],
            "level": "DEBUG",
        },
    },
}
