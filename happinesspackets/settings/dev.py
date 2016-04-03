# -*- coding: utf-8 -*-
# noinspection PyUnresolvedReferences
from .base import *  # noqa

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True
CRISPY_FAIL_SILENTLY = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_DIR.child('db.sqlite3'),
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 2525
SECRET_KEY = 'only-for-testing'

INTERNAL_IPS = ('127.0.0.1',)

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

ADMIN_ENABLED = True

MIDDLEWARE_CLASSES = [
    'happinesspackets.utils.middleware.SetRemoteAddrFromForwardedFor',
    'dogslow.WatchdogMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS += (
    'debug_toolbar',
)

SELENIUM_SCREENSHOT_DIR = PROJECT_DIR.child('selenium-screenshots')
