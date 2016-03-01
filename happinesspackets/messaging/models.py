# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from model_utils import Choices

from happinesspackets.utils.misc import readable_random_token
from django.db import models
from model_utils.models import TimeStampedModel

logger = logging.getLogger(__name__)


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
    sender_email_token = models.CharField(max_length=255, db_index=True)
    sender_ip = models.GenericIPAddressField()

    recipient_name = models.CharField(max_length=255)
    recipient_email = models.EmailField()

    message = models.TextField()

    sender_named = models.BooleanField(default=False)
    sender_approved_public = models.BooleanField(default=False)
    sender_approved_public_named = models.BooleanField(default=False)
    recipient_approved_public = models.BooleanField(default=False)
    recipient_approved_public_named = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk or force_insert:
            self.identifier = readable_random_token(alphanumeric=True)
            while Message.objects.filter(identifier=self.identifier).count():
                self.identifier = readable_random_token(alphanumeric=True)  # pragma: no cover
        return super(Message, self).save(force_insert, force_update, using, update_fields)
