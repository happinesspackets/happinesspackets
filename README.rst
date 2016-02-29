oslove
===============================

Open Source community love notes

To run this project or the tests, you'll have to set up a virtualenv, install the dev requirements and set
the right ``DJANGO_SETTINGS_MODULE``::

    virtualenv --no-site-packages --prompt='(oslove)' virtualenv/
    source virtualenv/bin/activate
    pip install -r requirements/dev.txt
    export DJANGO_SETTINGS_MODULE=oslove.settings.dev
    ./t

The ``t`` command is a very short shell script to run the tests with the right settings and report on coverage.

To run the integration tests::

    ./manage.py test -v 2 -p integration_test*.py --settings=oslove.settings.tsting

This repo contains some documentation directly relating to the code, and is built with Sphinx. To build it::

    cd docs
    make html
    open _build/html/index.html

