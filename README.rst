Open-source Happiness Packets
=============================

*******************
Goal of the Project
*******************  
Fedora Happiness Packet is a initiative that will help people or specially
fedora open source developers to acknowledge their contributions.There are many 
people are unaware of how loved, appreciated, or admired they are by
their peers. With this project, we are trying to create a friendly tool for people
to send positive feedback, thanks, or just a kind word to their peers, which people 
will love to use.

Want to make some changes or implement your own ideas in this project? This is an 
open source project. We will be very happy if yo do some changes and share your ideas!


Requirements
************
1. set up a virtualenv
2. install the dev requirements and set
   the correct ``DJANGO_SETTINGS_MODULE``, for example with::

        virtualenv --no-site-packages --prompt='(happinesspackets)' virtualenv/
        source virtualenv/bin/activate
        pip install -r requirements/dev.txt
        export DJANGO_SETTINGS_MODULE=happinesspackets.settings.dev
        ./t

    The ``t`` command is a very short shell script that runs the tests with the correct settings and reports on coverage.

3. run the integration tests::

        ./manage.py test -v 2 -p integration_test*.py --settings=happinesspackets.settings.tsting


For GSoC 2018 Applicants
************************

Skills you need
---------------
1. Python 
2. HTML/CSS/JS 
3. UI UX skills graphic design
4. knowledge of fedmsg optional: Cloud / Ansible,

https://docs.fedoraproject.org/mentored-projects/gsoc/2018/ideas.html#fedora-packets-fedora-happiness-packets
Go to this link and you will find the Informations about the Happiness packets project and other requirements.
