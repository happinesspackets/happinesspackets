from __future__ import unicode_literals

import django
from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin

urlpatterns = [
    path('', include('happinesspackets.messaging.urls', namespace="messaging")),
]

# if settings.ADMIN_ENABLED or settings.DEBUG:
#     urlpatterns.append(path('drunken-octo-lama/', include(admin.site.urls)))
