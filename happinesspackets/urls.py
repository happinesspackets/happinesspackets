from __future__ import unicode_literals

import django
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('happinesspackets.messaging.urls', namespace="messaging")),
]

if settings.ADMIN_ENABLED or settings.DEBUG:
    urlpatterns.append(url(r'^drunken-octo-lama/', include(admin.site.urls)))
    
    
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]


if settings.DEBUG:
    urlpatterns.append(url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}))
