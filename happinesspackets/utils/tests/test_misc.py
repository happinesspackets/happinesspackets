from __future__ import unicode_literals
from unittest import TestCase

from ..misc import readable_random_token


class ReadableRandomTokenTest(TestCase):
    def test_random_token(self):
        token1 = readable_random_token()
        token2 = readable_random_token()
        self.assertNotEqual(token1, token2)
        self.assertTrue('-' in token1)
        self.assertFalse(' ' in token1)
        self.assertTrue(' - ' in readable_random_token(add_spaces=True))
        self.assertFalse('1' in readable_random_token(alphanumeric=True))

        self.assertEqual(len(token1), 19)
        self.assertEqual(len(readable_random_token(short_token=True)), 9)
        self.assertEqual(len(readable_random_token(long_token=True)), 39)
