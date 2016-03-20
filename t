export DJANGO_SETTINGS_MODULE=happinesspackets.settings.tsting &&
OPBEAT_DISABLE_SEND=true coverage run ./manage.py test $@ &&
coverage report --fail-under=100
