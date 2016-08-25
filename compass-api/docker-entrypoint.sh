#!/bin/bash
set -e
cd ${HOME}/G4SE
python3 manage.py migrate --no-input
python3 manage.py collectstatic --noinput

/usr/local/bin/gunicorn G4SE.wsgi:application \
    --bind 0.0.0.0:8000
exec "$@"