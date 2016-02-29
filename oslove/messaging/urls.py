from __future__ import unicode_literals

from django.conf.urls import url

from .views import (ExampleFormView, StartView)

urlpatterns = [
    url(r'^$', StartView.as_view(), name='start'),
    url(r'^example/$', ExampleFormView.as_view(), name='example_form_view'),
]
