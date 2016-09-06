#!/bin/bash
set -e

if [ ! -f /src/settings.py ]; then
	echo DATABASE_URL = \'${DATABASE_URL}\' >> /src/settings.py
	echo FILESHARE_URL = \'${FILESHARE_URL}\' >> /src/settings.py
fi

/wait-for-it.sh -t 30 database:5432

/usr/bin/python3 /src/harvest_records.py /harvested-files/
cron -f
