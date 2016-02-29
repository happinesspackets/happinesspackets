from __future__ import unicode_literals

from django.conf.urls import url

from .views import (ExampleFormView)

urlpatterns = [
    url(r'^example/$', ExampleFormView.as_view(), name='example_form_view'),
]
