#!/bin/bash
set -e
cd /G4SE
/bin/wait-for-it.sh -t 30 database:5432
/bin/wait-for-it.sh -t 30 elasticsearch:9200
exec "$@"
