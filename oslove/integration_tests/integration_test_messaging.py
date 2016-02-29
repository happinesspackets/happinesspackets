# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from .utils import BaseTestCase


class MessagingIntegrationTest(BaseTestCase):
    screenshot_dir_suffix = 'messaging'

    def test_messaging_start(self):
        self.d.get('%s%s' % (self.live_server_url, reverse('messaging:start')))

        ################################
        # Start page
        self.wait_for_element(tag_name='h2', tag_text='What is open source community love notes?')
        self.d.save_screenshot(self.screenshot_dir.child('messaging_start_01.png'))

        self.d.find_element_by_link_text("Send a message").click()

        ################################
        # New message
        self.wait_for_element(tag_name='h2', tag_text='Send a message')

        self.d.find_element_by_name('sender_name').send_keys('Erik Romijn')
        self.d.find_element_by_name('sender_email').send_keys('sender@erik.io')
        self.d.find_element_by_name('recipient_name').send_keys('Mikey Ariel')
        self.d.find_element_by_name('recipient_email').send_keys('recipient@erik.io')
        self.d.find_element_by_name('message').send_keys("You're awesome")
        self.d.find_element_by_name('sender_named').click()

        self.d.save_screenshot(self.screenshot_dir.child('messaging_form_01.png'))
        self.d.find_element_by_name('submit').click()

        # TODO: check for database objects being created here

        ################################
        # End back on start page
        self.wait_for_element(tag_name='h2', tag_text='What is open source community love notes?')
