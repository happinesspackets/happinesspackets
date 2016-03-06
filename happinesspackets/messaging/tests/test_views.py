# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from .test_models import MessageModelFactory
from ..models import Message


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
        self.assertRedirects(response, reverse('messaging:sender_confirmation_sent'))

        self.assertEqual(len(mail.outbox), 1)
        message = Message.objects.get()
        self.assertEqual(message.status, Message.STATUS.pending_sender_confirmation)
        self.assertEqual(mail.outbox[0].recipients(), [message.sender_email])
        self.assertTrue(message.identifier in mail.outbox[0].body)
        self.assertTrue(message.sender_email_token in mail.outbox[0].body)

    def test_post_invalid_conflicting_publicity(self):
        self.post_data['sender_approved_public'] = False
        response = self.client.post(self.url, self.post_data)
        self.assertEqual(response.status_code, 200)


class MessageSentViewTest(TestCase):
    url = reverse('messaging:sender_confirmation_sent')

    def test_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class MessageSenderConfirmationView(TestCase):
    url_name = 'messaging:sender_confirm'

    def setUp(self):
        self.message = MessageModelFactory(sender_email_token='a-b-c', status=Message.STATUS.pending_sender_confirmation)
        url_kwargs = {'identifier': self.message.identifier, 'token': self.message.sender_email_token}
        self.url = reverse(self.url_name, kwargs=url_kwargs)

    def test_confirm_anonymous(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('messaging:sender_confirmed'))

        self.assertEqual(len(mail.outbox), 1)
        self.message.refresh_from_db()
        self.assertEqual(self.message.status, Message.STATUS.sent)
        self.assertEqual(mail.outbox[0].recipients(), [self.message.recipient_email])
        self.assertFalse(self.message.sender_name in mail.outbox[0].body)
        self.assertTrue(self.message.identifier in mail.outbox[0].body)
        self.assertTrue(self.message.recipient_email_token in mail.outbox[0].body)

    def test_confirm_named(self):
        self.message.sender_named = True
        self.message.save()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('messaging:sender_confirmed'))

        self.assertEqual(len(mail.outbox), 1)
        self.message.refresh_from_db()
        self.assertTrue(mail.outbox[0].recipients(), [self.message.recipient_email])
        self.assertTrue(self.message.sender_name in mail.outbox[0].body)
        self.assertTrue(self.message.identifier in mail.outbox[0].body)

    def test_bad_token(self):
        self.message.sender_email_token = 'o-t-h-e-r'
        self.message.recipient_email_token = 'a-b-c'
        self.message.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['not_found'])

    def test_bad_status(self):
        self.message.status = Message.STATUS.sent
        self.message.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['already_confirmed'])


class MessageSenderConfirmedView(TestCase):
    url = reverse('messaging:sender_confirmed')

    def test_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class MessageRecipientMessageUpdate(TestCase):
    url_name = 'messaging:recipient_message_update'

    def setUp(self):
        self.message = MessageModelFactory(recipient_email_token='a-b-c', status=Message.STATUS.sent)
        url_kwargs = {'identifier': self.message.identifier, 'token': self.message.recipient_email_token}
        self.url = reverse(self.url_name, kwargs=url_kwargs)

    def test_confirm(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_valid(self):
        self.assertFalse(self.message.recipient_approved_public)
        response = self.client.post(self.url, {'recipient_approved_public': True})
        self.assertRedirects(response, self.url)
        self.message.refresh_from_db()
        self.assertTrue(self.message.recipient_approved_public)

    def test_post_invalid(self):
        self.assertFalse(self.message.recipient_approved_public_named)
        response = self.client.post(self.url, {'recipient_approved_public_named': True})
        self.assertEqual(response.status_code, 200)
        self.message.refresh_from_db()
        self.assertFalse(self.message.recipient_approved_public_named)

    def test_bad_token(self):
        self.message.sender_email_token = 'a-b-c'
        self.message.recipient_email_token = 'o-t-h-e-r'
        self.message.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_bad_status(self):
        self.message.status = Message.STATUS.pending_sender_confirmation
        self.message.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
