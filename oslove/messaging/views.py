# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView

from .forms import MessageSendForm

logger = logging.getLogger(__name__)


class StartView(TemplateView):
    template_name = 'messaging/start.html'


class MessageSendView(FormView):
    template_name = 'messaging/message_send_form.html'
    form_class = MessageSendForm

    def dispatch(self, *args, **kwargs):
        return super(MessageSendView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        logger.info('[%s] input sent to form' % (self.request.META['REMOTE_ADDR']))
        # TODO: save the message and send the confirmation mail
        return HttpResponseRedirect(reverse('messaging:start'))   # TODO: make a post message sending page
