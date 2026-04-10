Open-source Happiness Packets
=============================

The Open-Source Happiness Packets project was created by `Sasha
Romijn <https://twitter.com/mxsash>`__ and `Mikey
Ariel <https://twitter.com/thatdocslady>`__ in March 2016. The idea came
about while we were building our `Healthy Minds in a Healthy
Community <https://github.com/erikr/well-being/>`__ presentation for
`Djangocon Europe 2016 <https://2016.djangocon.eu/speakers/13>`__. One
of the issues we wanted to address in the presentation was that many
people are unaware of how loved, appreciated, or admired they are by
their peers, since our culture seems to discourage positive feedback and
amplify negative feedback. With this project, we wanted to provide a
platform for people to send positive feedback, thanks, or just a kind
word to their peers, with hope to make it easier and more acceptable for
people to spread happiness, gratitude and appreciation in open-source
communities.

The structure and format of the site is basic, and contributions are
welcome!

To run this project or the tests, you need `uv <https://docs.astral.sh/uv/>`_ installed::

    uv sync
    export DJANGO_SETTINGS_MODULE=happinesspackets.settings.dev
    uv run python manage.py test
