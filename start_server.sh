#!/usr/bin/env bash

# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd cfviewer; python manage.py createsuperuser --no-input)
fi
(cd cfviewer; python3 manage.py collectstatic --noinput; python3 manage.py makemigrations; python3 manage.py migrate; python3 manage.py updater; gunicorn CFViewer.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"