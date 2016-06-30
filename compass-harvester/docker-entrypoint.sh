#!/bin/bash
set -e

if [ ! -f /src/settings.py ]; then
	echo $DATA_PROVIDER_URL
	echo $METADATA_FORMAT
	oai-reg add eprints ${DATA_PROVIDER_URL}  --metadataPrefix ${METADATA_FORMAT} --dir /harvested-files/

	echo DATABASE_URL = \'${DATABASE_URL}\' >> /src/settings.py
fi

/usr/bin/python /src/harvest_records.py /harvested-files/
cron -f
