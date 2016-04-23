import os

from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured
from unipath import Path

PROJECT_DIR = Path(__file__).ancestor(3)

# For clean_pyc to work without complaining
BASE_DIR = PROJECT_DIR

DEBUG = False

ADMINS = (
    ('Erik Romijn', 'github@erik.io'),
)
SERVER_EMAIL = ADMINS[0][1]

DEFAULT_FROM_EMAIL = "Happiness Packets <info@happinesspackets.io>"

EMAIL_SUBJECT_PREFIX = "[happinesspackets] "

DOGSLOW_TIMER = 15
DOGSLOW_LOG_TO_FILE = False
DOGSLOW_LOGGER = 'dogslow'

TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'en-GB'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATE_FORMAT = 'j F Y'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = "PHPSESSID"
CSRF_COOKIE_NAME = "JSESSIONID"

ADMIN_ENABLED = False
MAX_MESSAGES = 20

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}


MEDIA_ROOT = PROJECT_DIR.child('media')
MEDIA_URL = '/media/'
STATIC_ROOT = PROJECT_DIR.child('static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_DIR.child('assets'),
)

# noinspection PyUnresolvedReferences
MIDDLEWARE_CLASSES = [
    'happinesspackets.utils.middleware.SetRemoteAddrFromForwardedFor',
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'dogslow.WatchdogMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'happinesspackets.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'happinesspackets.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_DIR.child('templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admin',
    'django.contrib.humanize',

    'django_extensions',
    'crispy_forms',
    'happinesspackets.messaging',
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s gunicorn[%(process)d]: %(levelname)s %(name)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(name)s: %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'requests.packages.urllib3.connectionpool': {
            'handlers': ['null'],
            'propagate': False,
        },
        'stripe': {
            'handlers': ['null'],
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)
