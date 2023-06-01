# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import factory
from django.test import TestCase
from factory.django import DjangoModelFactory


class MessageModelFactory(DjangoModelFactory):
    class Meta:
        model = 'messaging.Message'

    sender_name = 'Sender sender'
    sender_email = 'sendersender@null'
    recipient_name = 'Recipient recipient'
    recipient_email = 'recipientrecipient+foo@null'
    sender_ip = '127.0.0.1'
    message = 'message content'


class BlacklistedEmailFactory(DjangoModelFactory):
    class Meta:
        model = 'messaging.BlacklistedEmail'

    email = 'emailemail@null'
    confirmation_ip = '127.0.0.1'


class MessageModelTest(TestCase):
    def test_unique_identifier(self):
        obj1 = MessageModelFactory()
        obj2 = MessageModelFactory()
        self.assertNotEqual(obj1.identifier, obj2.identifier)
