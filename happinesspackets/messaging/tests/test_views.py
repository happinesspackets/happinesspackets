# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.crypto import salted_hmac

from .test_models import MessageModelFactory, BlacklistedEmailFactory
from ..models import Message, BLACKLIST_HMAC_SALT, BlacklistedEmail


class StartViewTest(TestCase):
    url = reverse('messaging:start')

    def test_renders(self):
        MessageModelFactory(sender_approved_public=True, sender_approved_public_named=False,
                            recipient_approved_public=True, recipient_approved_public_named=True,
                            admin_approved_public=True)
        msg = MessageModelFactory(sender_approved_public=True, sender_approved_public_named=True,
                                  recipient_approved_public=True, recipient_approved_public_named=False,
                                  admin_approved_public=True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, msg.sender_name)
        self.assertNotContains(response, msg.recipient_name)
        self.assertContains(response, msg.message)
        self.assertNotContains(response, msg.sender_email)
        self.assertNotContains(response, msg.recipient_email)


class FaqViewTest(TestCase):
    url = reverse('messaging:faq')

    def test_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class InspirationViewTest(TestCase):
    url = reverse('messaging:inspiration')

    def test_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class ArchiveViewTest(TestCase):
    url = reverse('messaging:archive')

    def test_renders_no_public_messages(self):
        MessageModelFactory(sender_approved_public=True, sender_approved_public_named=True,
                            recipient_approved_public=True, recipient_approved_public_named=True,
                            admin_approved_public=False)
        MessageModelFactory(sender_approved_public=False, sender_approved_public_named=True,
                            recipient_approved_public=True, recipient_approved_public_named=True,
                            admin_approved_public=True)
        MessageModelFactory(sender_approved_public=True, sender_approved_public_named=True,
                            recipient_approved_public=False, recipient_approved_public_named=True,
                            admin_approved_public=True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['message_list'].count())

    def test_renders_named_messages(self):
        msg = MessageModelFactory(sender_approved_public=True, sender_approved_public_named=True,
                                  recipient_approved_public=True, recipient_approved_public_named=True,
                                  admin_approved_public=True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, msg.sender_name)
        self.assertContains(response, msg.recipient_name)
        self.assertContains(response, msg.message)
        self.assertNotContains(response, msg.sender_email)
        self.assertNotContains(response, msg.recipient_email)

    def test_renders_unnamed_messages(self):
        MessageModelFactory(sender_approved_public=True, sender_approved_public_named=False,
                            recipient_approved_public=True, recipient_approved_public_named=True,
                            admin_approved_public=True)
        msg = MessageModelFactory(sender_approved_public=True, sender_approved_public_named=True,
                                  recipient_approved_public=True, recipient_approved_public_named=False,
                                  admin_approved_public=True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, msg.sender_name)
        self.assertNotContains(response, msg.recipient_name)
        self.assertContains(response, msg.message)
        self.assertNotContains(response, msg.sender_email)
        self.assertNotContains(response, msg.recipient_email)


class BlacklistViewTest(TestCase):
    url_name = 'messaging:blacklist_email'

    def setUp(self):
        self.message = MessageModelFactory()
        self.correct_digest = salted_hmac(BLACKLIST_HMAC_SALT, self.message.recipient_email).hexdigest()
        self.url_kwargs = {'email': self.message.recipient_email, 'digest': self.correct_digest}
        self.url = reverse(self.url_name, kwargs=self.url_kwargs)

    def test_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_confirm(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('messaging:start'))
        obj = BlacklistedEmail.objects.get()
        self.assertEqual(obj.email, self.message.recipient_email)
        self.assertEqual(obj.stripped_email, 'recipientrecipient@null')

    def test_validates_digest(self):
        self.url_kwargs['email'] = self.message.sender_email
        self.url = reverse(self.url_name, kwargs=self.url_kwargs)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(BlacklistedEmail.objects.count())


class SendViewTest(TestCase):
    url = reverse('messaging:send')

    def setUp(self):
        super(SendViewTest, self).setUp()
        self.post_data = {
            'sender_name': 'sender name',
            'sender_email': 'SEN.DER+FOOBAR@erik.io',
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
        self.assertEqual(len(response.context['form'].errors), 1)
        self.assertEqual(len(mail.outbox), 0)

    def test_post_blacklisted_sender(self):
        BlacklistedEmailFactory(email='sender@erik.io', stripped_email='sender@erikio')
        response = self.client.post(self.url, self.post_data)
        self.assertRedirects(response, reverse('messaging:sender_confirmation_sent'))
        self.assertEqual(len(mail.outbox), 0)

    def test_post_ratelimited_sender(self):
        for i in range(settings.MAX_MESSAGES + 1):
            MessageModelFactory(sender_email='sender@erik.io', sender_email_stripped='sender@erikio')
        response = self.client.post(self.url, self.post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['form'].errors), 1)
        self.assertEqual(len(mail.outbox), 0)

    def test_post_ratelimited_recipient(self):
        for i in range(settings.MAX_MESSAGES + 1):
            MessageModelFactory(recipient_email='sender@erik.io', recipient_email_stripped='recipient@erikio')
        response = self.client.post(self.url, self.post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['form'].errors), 1)
        self.assertEqual(len(mail.outbox), 0)


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
        self.assertFalse(self.message.sender_email in mail.outbox[0].body)
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

    def test_confirm_blacklisted_recipient(self):
        BlacklistedEmailFactory(email='recipient@erik.io', stripped_email='recipientrecipient@null')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('messaging:sender_confirmed'))
        self.assertEqual(len(mail.outbox), 0)


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
