# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from .forms import ExampleForm

logger = logging.getLogger(__name__)


class ExampleFormView(FormView):
    template_name = 'messaging/example_form.html'
    form_class = ExampleForm

    def dispatch(self, *args, **kwargs):
        return super(ExampleFormView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        logger.info('[%s] input sent to form' % (self.request.META['REMOTE_ADDR']))
        return HttpResponseRedirect(reverse('messaging:example_form_view'))
