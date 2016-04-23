# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import re

from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils.crypto import salted_hmac
from model_utils import Choices
from model_utils.models import TimeStampedModel

from happinesspackets.utils.misc import readable_random_token, send_html_mail

logger = logging.getLogger(__name__)
BLACKLIST_HMAC_SALT = 'happinesspackets.messaging.views.BlacklistEmailView'


class Message(TimeStampedModel):
    STATUS = Choices(
        'pending_sender_confirmation',
        'sent',
        'read',
    )

    identifier = models.CharField(max_length=255, db_index=True)
    status = models.CharField(choices=STATUS, default=STATUS.pending_sender_confirmation, max_length=255)

    sender_name = models.CharField(max_length=255)
    sender_email = models.EmailField()
    sender_email_stripped = models.CharField(max_length=255)
    sender_email_token = models.CharField(max_length=255, db_index=True)
    sender_ip = models.GenericIPAddressField()

    recipient_name = models.CharField(max_length=255)
    recipient_email = models.EmailField()
    recipient_email_stripped = models.CharField(max_length=255)
    recipient_email_token = models.CharField(max_length=255, db_index=True)

    message = models.TextField()

    sender_named = models.BooleanField(default=False)
    sender_approved_public = models.BooleanField(default=False)
    sender_approved_public_named = models.BooleanField(default=False)
    recipient_approved_public = models.BooleanField(default=False)
    recipient_approved_public_named = models.BooleanField(default=False)

    admin_approved_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.sender_email_stripped = strip_email(self.sender_email)
        self.recipient_email_stripped = strip_email(self.recipient_email)
        if not self.pk or force_insert:
            self.identifier = readable_random_token(alphanumeric=True)
            while Message.objects.filter(identifier=self.identifier).count():
                self.identifier = readable_random_token(alphanumeric=True)  # pragma: no cover
        return super(Message, self).save(force_insert, force_update, using, update_fields)

    def send_sender_confirmation(self, use_https, domain):
        stripped_email = strip_email(self.sender_email)
        if BlacklistedEmail.objects.filter(stripped_email=stripped_email).count():
            return

        blacklist_digest = salted_hmac(BLACKLIST_HMAC_SALT, self.sender_email).hexdigest()
        blacklist_url = reverse('messaging:blacklist_email', kwargs={'email': self.sender_email, 'digest': blacklist_digest})
        self.sender_email_token = readable_random_token(alphanumeric=True)
        context = {
            'message': self,
            'protocol': 'https' if use_https else 'http',
            'domain': domain,
            'recipient': self.sender_email,
            'blacklist_url': blacklist_url,
        }
        subject = render_to_string('messaging/sender_confirmation_subject.txt', context)
        subject = ' '.join(subject.splitlines())
        body_txt = render_to_string('messaging/sender_confirmation_mail.txt', context)
        body_html = render_to_string('messaging/sender_confirmation_mail.html', context)
        send_html_mail(subject, body_txt, body_html, self.sender_email)
        self.save()

    def send_to_recipient(self, use_https, domain):
        stripped_email = strip_email(self.recipient_email)
        if BlacklistedEmail.objects.filter(stripped_email=stripped_email).count():
            return

        blacklist_digest = salted_hmac(BLACKLIST_HMAC_SALT, self.recipient_email).hexdigest()
        blacklist_url = reverse('messaging:blacklist_email', kwargs={'email': self.recipient_email, 'digest': blacklist_digest})
        self.recipient_email_token = readable_random_token(alphanumeric=True)
        self.status = Message.STATUS.sent
        context = {
            'message': self,
            'protocol': 'https' if use_https else 'http',
            'domain': domain,
            'recipient': self.recipient_email,
            'blacklist_url': blacklist_url,
        }
        subject = render_to_string('messaging/recipient_subject.txt', context)
        subject = ' '.join(subject.splitlines())
        body_txt = render_to_string('messaging/recipient_mail.txt', context)
        body_html = render_to_string('messaging/recipient_mail.html', context)
        send_html_mail(subject, body_txt, body_html, self.recipient_email)
        self.save()


class BlacklistedEmail(TimeStampedModel):
    email = models.EmailField()
    stripped_email = models.CharField(max_length=255)
    confirmation_ip = models.GenericIPAddressField()


def strip_email(email):
    return re.sub('[^@\w]', '', re.sub('\+\w+', '', email.lower()))
