#!/bin/bash
set -e
cd /G4SE
/bin/wait-for-it.sh -t 30 database:5432
python3 manage.py migrate --no-input
python3 manage.py collectstatic --noinput
/bin/wait-for-it.sh -t 30 elasticsearch:9200
python3 manage.py rebuild_index --noinput
exec "$@"
