# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from .utils import BaseTestCase


class ExampleIntegrationTest(BaseTestCase):
    screenshot_dir_suffix = 'messaging'

    def test_messaging(self):
        self.d.get('%s%s' % (self.live_server_url, reverse('messaging:example_form_view')))

        ################################
        # New submission
        self.wait_for_element(tag_name='h1', tag_text='Voorbeeldpagina')

        self.d.find_element_by_name('input').send_keys('voorbeeldinput')
        self.d.save_screenshot(self.screenshot_dir.child('messaging_01.png'))
        self.d.find_element_by_name('submit').click()

        ################################
        # End back on submission page
        self.wait_for_element(tag_name='h1', tag_text='Voorbeeldpagina')

        # Normally we'd check for database objects being created here.
