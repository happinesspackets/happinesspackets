export DJANGO_SETTINGS_MODULE=happinesspackets.settings.tsting &&
coverage run ./manage.py test $@ &&
coverage report --fail-under=100
