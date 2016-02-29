from __future__ import unicode_literals
from django.utils.crypto import get_random_string


def readable_random_token(alphanumeric=False, add_spaces=False, short_token=False, long_token=False):
    """
    Generate a random token that is also reasonably readable.

    Generates 4 segments of 4 characters, seperated by dashes. Can either use digits only (default),
    or non-confusing letters and digits (alphanumeric=True). If add_spaces is set, spaces are added
    around the groups. This is intended to prevent mobile phones that see e.g. "-3" as an emoticon.
    If short_token is set, the token is two segments of four characters.
    """
    segments = 4
    if short_token:
        segments = 2
    if long_token:
        segments = 8
    if alphanumeric:
        allowed_chars = "BCDFGHJLKMNPQRSTVWXYZ23456789"
    else:
        allowed_chars = "1234567890"
    elements = [get_random_string(length=4, allowed_chars=allowed_chars) for i in range(segments)]
    join_str = "-"
    if add_spaces:
        join_str = " - "
    return join_str.join(elements)
