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

    def test_messaging_form(self):
        self.d.get('%s%s' % (self.live_server_url, reverse('messaging:example_form_view')))

        ################################
        # New submission
        self.wait_for_element(tag_name='h2', tag_text='Voorbeeldpagina')

        self.d.find_element_by_name('input').send_keys('voorbeeldinput')
        self.d.save_screenshot(self.screenshot_dir.child('messaging_form_01.png'))
        self.d.find_element_by_name('submit').click()

        ################################
        # End back on submission page
        self.wait_for_element(tag_name='h2', tag_text='Voorbeeldpagina')

        # Normally we'd check for database objects being created here.
