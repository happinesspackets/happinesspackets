# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.test import TestCase


class StartViewTest(TestCase):
    url = reverse('messaging:start')

    def test_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class SendViewTest(TestCase):
    url = reverse('messaging:send')

    def setUp(self):
        super(SendViewTest, self).setUp()
        self.post_data = {
            'sender_name': 'sender name',
            'sender_email': 'sender@erik.io',
            'recipient_name': 'recipient name',
            'recipient_email': 'recipient@erik.io',
            'message': 'message',
            'sender_named': True,
            'sender_approved_public': True,
            'sender_approved_public_named': True,
        }

    def test_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_valid(self):
        response = self.client.post(self.url, self.post_data)
        self.assertRedirects(response, reverse('messaging:start'))

    def test_post_invalid_conflicting_publicity(self):
        self.post_data['sender_approved_public'] = False
        response = self.client.post(self.url, self.post_data)
        self.assertEqual(response.status_code, 200)
