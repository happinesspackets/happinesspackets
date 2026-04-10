import os

# noinspection PyUnresolvedReferences
from .base import *  # noqa

SECRET_KEY = os.getenv("SECRET_KEY")

SESSION_COOKIE_AGE = 3600 * 2

hostname = os.getenv("HOSTNAME", "")
ALLOWED_HOSTS = [hostname, "www." + hostname]

ADMIN_ENABLED = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": "host.docker.internal",
        "PORT": "5432",
        "CONN_MAX_AGE": None,
    }
}

TEMPLATES[0]["OPTIONS"]["loaders"] = (
    (
        "django.template.loaders.cached.Loader",
        (
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ),
    ),
)

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

DEFAULT_FROM_EMAIL = os.getenv(
    "EMAIL_FROM", "Happiness Packets <info@happinesspackets.io>"
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "in.mailjet.com")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = True
