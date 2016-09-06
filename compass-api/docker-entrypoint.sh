#!/bin/bash
set -e
cd /G4SE
touch /var/log/G4SE.log
/wait-for-it.sh -t 30 database:5432
python3 manage.py migrate --no-input
python3 manage.py collectstatic --noinput

exec "$@"
