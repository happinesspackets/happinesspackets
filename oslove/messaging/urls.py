from __future__ import unicode_literals

from django.conf.urls import url

from .views import (StartView, MessageSendView)

urlpatterns = [
    url(r'^$', StartView.as_view(), name='start'),
    url(r'^send/$', MessageSendView.as_view(), name='send'),
]
