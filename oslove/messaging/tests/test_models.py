# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
import factory


class ExampleModelFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'messaging.ExampleModel'

    status = 'rejected'


class ExampleModelTest(TestCase):
    def test_unique_identifier(self):
        obj1 = ExampleModelFactory()
        obj2 = ExampleModelFactory()
        self.assertNotEqual(obj1.identifier, obj2.identifier)
