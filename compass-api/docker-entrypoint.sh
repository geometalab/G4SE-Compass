#!/bin/bash
set -e
cd /G4SE
/bin/wait-for-it.sh -t 30 database:5432
yes "yes" | python ./manage.py migrate
python3 manage.py collectstatic --noinput
/bin/wait-for-it.sh -t 30 elasticsearch:9200
python3 manage.py rebuild_index --noinput
python3 manage.py retag_records
python3 manage.py update_index
exec "$@"
