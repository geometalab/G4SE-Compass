import shutil
import tempfile
import xml.etree.ElementTree as ET
from django.utils import timezone
from urllib import request
import csv
import io
import os

from dateutil.parser import parse

from api.models import HarvestedRecord

BASE_FILESHARE_URL = os.environ.get('FILESHARE_URL', 'https://geodata4edu.ethz.ch/metadata/')

WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

VALID_STATUS = '[Valid]'


def _geovite_id(record_name):
    id = record_name.split('.')[0]
    return 'oai:geovite.ethz.ch:' + id


def _remove_duplicate_entries():
    to_be_deleted = []
    for record in HarvestedRecord.objects.all():
        if HarvestedRecord.objects.filter(identifier=record.identifier).count() > 1:
            to_be_deleted.append(HarvestedRecord.objects.filter(identifier=record.identifier).exclude(api_id=record.api_id))
    for delete_em in to_be_deleted:
        delete_em.delete()


def read_xml(url):
    tree = ET.ElementTree(file=request.urlopen(BASE_FILESHARE_URL + url))
    root = tree.getroot()
    record = {}
    for child in root:
        content = child.text
        tag = child.tag.split('}', 1)[1]
        record[tag] = content
    record['login_name'] = 'GEOVITE_AUTOIMPORTER'
    record['title'] = record.pop('content')
    return record


def read_csv(file):
    reader = csv.reader(io.TextIOWrapper(file), delimiter=' ')
    return list(reader)


def create_new_record(record_name, modified):
    data = read_xml(record_name)
    data['modified'] = modified
    data['identifier'] = _geovite_id(record_name)
    print('creating entry {}'.format(data['identifier']))
    HarvestedRecord.objects.create(**data)


def update_record(record, record_xml, modified):
    data = read_xml(record_xml)
    data['modified'] = modified
    _ = data.pop('identifier', None)
    print('updating entry {}'.format(record.identifier))
    HarvestedRecord.objects.filter(api_id=record.api_id).update(**data)


def delete_obsolete_records(existing_record_identifiers):
    old_entries = HarvestedRecord.objects.exclude(identifier__in=existing_record_identifiers)
    count = len(old_entries)
    print('removing {} entries'.format(count))
    old_entries.delete()


def update_entry(entry):
    naive_datetime = parse(entry[2])
    datetime_kwargs = dict(
        year=naive_datetime.year,
        month=naive_datetime.month,
        day=naive_datetime.day,
        hour=naive_datetime.hour,
        minute=naive_datetime.minute,
        second=naive_datetime.second,
    )
    status, xml_file_name, last_modified = entry[0], entry[1], timezone.datetime(**datetime_kwargs)
    if status != VALID_STATUS:
        # all entries not matching are being deleted anyway
        return

    identifier = _geovite_id(xml_file_name)
    existing_record = HarvestedRecord.objects.filter(identifier=identifier).first()
    if existing_record is not None:
        update_record(existing_record, xml_file_name, last_modified)
    else:
        create_new_record(xml_file_name, last_modified)
    return identifier


def update_harvested_records():
    existing_record_identifiers = []

    with tempfile.NamedTemporaryFile() as metadata_csv:
        request.urlretrieve(BASE_FILESHARE_URL + "metadata.csv", metadata_csv.name)
        data = read_csv(metadata_csv)
        for entry in data[1:]:
            identifier = update_entry(entry)
            if identifier:
                existing_record_identifiers.append(identifier)
    delete_obsolete_records(existing_record_identifiers)


def harvest():
    _remove_duplicate_entries()
    update_harvested_records()
