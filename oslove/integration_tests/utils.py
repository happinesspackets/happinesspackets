from __future__ import unicode_literals

import time

from django.conf import settings
from django.test import LiveServerTestCase
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver


class BaseTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.d = WebDriver()
        # settings.DEBUG = True
        super(BaseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.d.quit()
        super(BaseTestCase, cls).tearDownClass()

    def setUp(self):
        super(BaseTestCase, self).setUp()

        self.screenshot_dir = settings.SELENIUM_SCREENSHOT_DIR.child(self.screenshot_dir_suffix)
        self.screenshot_dir.mkdir(parents=True)

        self.d.set_window_size('1200', '1200')

    def wait_for_element(self, tag_id=None, tag_name=None, tag_text=None):
        if tag_id and (tag_name or tag_text):
            raise Exception('tag_id can not be used with either tag_name or tag_text')
        if not tag_id and not tag_name:
            raise Exception('You must provide either tag_id or tag_name')

        attempts = 0
        while attempts < 100:  # 10 seconds
            if tag_name:
                try:
                    tag = self.d.find_element_by_tag_name(tag_name)
                    if not tag_text or tag.text == tag_text:
                        return tag
                except NoSuchElementException:
                    pass
            if tag_id:
                try:
                    return self.d.find_element_by_id(tag_id)
                except NoSuchElementException:
                    pass
            time.sleep(0.1)
            attempts += 1
        self.d.save_screenshot(self.screenshot_dir.child('assertion-failure.png'))
        raise AssertionError("Unable to find element %s%s after 10 seconds: screenshot saved" % (tag_id, tag_name))
