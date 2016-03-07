# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView, UpdateView

from .models import Message
from .forms import MessageSendForm, MessageRecipientForm

logger = logging.getLogger(__name__)


class StartView(TemplateView):
    template_name = 'messaging/start.html'


class FaqView(TemplateView):
    template_name = 'messaging/faq.html'


class MessageSendView(FormView):
    template_name = 'messaging/message_send_form.html'
    form_class = MessageSendForm

    def dispatch(self, *args, **kwargs):
        return super(MessageSendView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        message = form.save(commit=False)
        message.sender_ip = self.request.META['REMOTE_ADDR']
        message.save()
        message.send_sender_confirmation(self.request.is_secure(), self.request.get_host())
        return HttpResponseRedirect(reverse('messaging:sender_confirmation_sent'))


class MessageSenderConfirmationSentView(TemplateView):
    template_name = 'messaging/message_sender_confirmation_sent.html'


class MessageSenderConfirmationView(TemplateView):
    template_name = 'messaging/message_sender_confirmation_failed.html'

    def get(self, request, *args, **kwargs):
        try:
            message = Message.objects.get(identifier=kwargs['identifier'], sender_email_token=kwargs['token'])
        except Message.DoesNotExist:
            return self.render_to_response({'not_found': True})

        if message.status != Message.STATUS.pending_sender_confirmation:
            return self.render_to_response({'already_confirmed': True})

        message.send_to_recipient(self.request.is_secure(), self.request.get_host())
        return HttpResponseRedirect(reverse('messaging:sender_confirmed'))


class MessageSenderConfirmedView(TemplateView):
    template_name = 'messaging/message_sender_confirmed.html'


class MessageRecipientMessageUpdate(UpdateView):
    model = Message
    form_class = MessageRecipientForm
    template_name = 'messaging/message_recipient_form.html'
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'

    def get_queryset(self):
        message = super(MessageRecipientMessageUpdate, self).get_queryset()
        valid_status = [Message.STATUS.sent, Message.STATUS.read]
        return message.filter(recipient_email_token=self.kwargs['token'], status__in=valid_status)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your choices have been saved.")
        return HttpResponseRedirect(self.request.path)
