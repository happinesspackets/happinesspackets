happinesspackets
===============================

Open-source Happiness Packets project

This project was created for DjangoCon Europe 2016. The structure and format of the site is basic, and
contributions are welcome!

To run this project or the tests, you need to set up a virtualenv, install the dev requirements and set
the correct ``DJANGO_SETTINGS_MODULE``::

    virtualenv --no-site-packages --prompt='(happinesspackets)' virtualenv/
    source virtualenv/bin/activate
    pip install -r requirements/dev.txt
    export DJANGO_SETTINGS_MODULE=happinesspackets.settings.dev
    ./t

The ``t`` command is a very short shell script that runs the tests with the correct settings and reports on coverage.

To run the integration tests::

    ./manage.py test -v 2 -p integration_test*.py --settings=happinesspackets.settings.tsting

This repository contains some documentation directly related to the code, built with Sphinx. To build the docs::

    cd docs
    make html
    open _build/html/index.html
