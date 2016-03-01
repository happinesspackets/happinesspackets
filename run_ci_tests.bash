#!/bin/bash -x
# This is a simple script to run our integration tests in parallel on CircleCI. This will be called from circle.yml.
# At this time, the script only works for having two nodes.

export DB_NAME="circle_test_"$CIRCLE_NODE_INDEX
ret=0

case $CIRCLE_NODE_INDEX in
    0)
    flake8 happinesspackets || ret=$?
    ./manage.py makemigrations --dry-run --noinput | grep -i 'no changes detected' || ret=$?

    coverage run ./manage.py test -v 2 --noinput && coverage html --fail-under=90 || ret=$?
    ;;

    1)
    ./manage.py test -v 2 -p integration_test*.py --settings=happinesspackets.settings.ci --noinput || ret=$?
    ;;
esac

exit $ret



