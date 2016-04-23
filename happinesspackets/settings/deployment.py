# noinspection PyUnresolvedReferences
from .base import *  # noqa

SECRET_KEY = get_env_variable("SECRET_KEY")

SESSION_COOKIE_AGE = 3600 * 2

ALLOWED_HOSTS = get_env_variable('DJANGO_ALLOWED_HOSTS').split(',')

ADMIN_ENABLED = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable("DB_NAME"),
        'USER': get_env_variable("DB_USERNAME"),
        'PASSWORD': get_env_variable("DB_PASSWORD"),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 300,
    }
}

INSTALLED_APPS.append('opbeat.contrib.django')

TEMPLATES[0]['OPTIONS']['loaders'] = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

LOGGING['handlers']['file'] = {
    'level': 'INFO',
    'class': 'logging.handlers.WatchedFileHandler',
    'formatter': 'verbose',
    'filename': get_env_variable("DJANGO_LOGFILE"),
}

LOGGING['loggers']['']['handlers'].append('file')

EMAIL_HOST = 'in.mailjet.com'
EMAIL_HOST_USER = get_env_variable('EMAIL_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_PASSWORD')
EMAIL_USE_TLS = True
