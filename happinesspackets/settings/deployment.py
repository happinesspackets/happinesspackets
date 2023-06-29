import dj_database_url

# noinspection PyUnresolvedReferences
from .base import *  # noqa

SECRET_KEY = get_env_variable("SECRET_KEY")

SESSION_COOKIE_AGE = 3600 * 2

ALLOWED_HOSTS = ["happinesspackets.fly.dev", ".happinesspackets.io"]

ADMIN_ENABLED = True

DATABASES = {
    'default':
        dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
        )
}

TEMPLATES[0]['OPTIONS']['loaders'] = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

EMAIL_HOST = 'in.mailjet.com'
EMAIL_HOST_USER = get_env_variable('EMAIL_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_PASSWORD')
EMAIL_USE_TLS = True
