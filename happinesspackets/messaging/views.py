# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.utils.crypto import salted_hmac, constant_time_compare
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView, UpdateView, ListView

from .forms import MessageSendForm, MessageRecipientForm
from .models import Message, BLACKLIST_HMAC_SALT, BlacklistedEmail, strip_email

logger = logging.getLogger(__name__)


class ArchiveListView(ListView):
    model = Message

    def get_queryset(self):
        queryset = super(ArchiveListView, self).get_queryset()
        return queryset.filter(sender_approved_public=True, recipient_approved_public=True, admin_approved_public=True)


class StartView(ArchiveListView):
    template_name = 'messaging/start.html'

    def get_queryset(self):
        return super(StartView, self).get_queryset().order_by('?')[:2]


class FaqView(TemplateView):
    template_name = 'messaging/faq.html'


class ArchiveView(ArchiveListView):
    template_name = 'messaging/archive.html'


class InspirationView(TemplateView):
    template_name = 'messaging/inspiration.html'


class BlacklistEmail(object):
    pass


class BlacklistEmailView(TemplateView):
    success_url = reverse_lazy('messaging:start')
    template_name = 'messaging/blacklist_email.html'

    def get_email(self):
        expected_digest = salted_hmac(BLACKLIST_HMAC_SALT, self.kwargs['email'])
        if not constant_time_compare(expected_digest.hexdigest(), self.kwargs['digest']):
            raise Http404
        return self.kwargs['email']

    def get_context_data(self, **kwargs):
        context = super(BlacklistEmailView, self).get_context_data(**kwargs)
        context['email'] = self.get_email()
        return context

    def post(self, request, *args, **kwargs):
        email = self.get_email()
        stripped_email = strip_email(email)
        BlacklistedEmail.objects.create(email=email, stripped_email=stripped_email, confirmation_ip=self.request.META['REMOTE_ADDR'])
        message = format_html("We've blacklisted your address and will never email <em>{0}</em> again. Sorry to have bothered you!", email)
        messages.success(self.request, message)
        return HttpResponseRedirect(self.success_url)


class MessageSendView(FormView):
    template_name = 'messaging/message_send_form.html'
    form_class = MessageSendForm

    @method_decorator(sensitive_post_parameters('message'))
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
