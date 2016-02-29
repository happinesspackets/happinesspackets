# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
import factory


class MessageModelFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'messaging.Message'

    sender_ip = '127.0.0.1'


class MessageModelTest(TestCase):
    def test_unique_identifier(self):
        obj1 = MessageModelFactory()
        obj2 = MessageModelFactory()
        self.assertNotEqual(obj1.identifier, obj2.identifier)
