# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.test import TestCase


class ExampleFormViewTest(TestCase):
    url = reverse('messaging:example_form_view')

    def test_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_valid(self):
        response = self.client.post(self.url, {'input': 'test input'})
        self.assertRedirects(response, self.url)

    def test_post_invalid_empty_input(self):
        response = self.client.post(self.url, {'input': ''})
        self.assertEqual(response.status_code, 200)
