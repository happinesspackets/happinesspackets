# noinspection PyUnresolvedReferences
from .deployment import *  # noqa

# This is intended to mimic production as close as possible regarding databases and such.

# Use the same database for tests as live, used for celery interactions
DATABASES['default']['TEST'] = DATABASES['default']

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

DATABASES['default']['CONN_MAX_AGE'] = 0

SELENIUM_SCREENSHOT_DIR = PROJECT_DIR.child('selenium-screenshots')
