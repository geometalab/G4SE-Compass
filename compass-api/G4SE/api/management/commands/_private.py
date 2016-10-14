import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

from django.utils import timezone
from urllib import request
import os

from api.models import GeoServiceMetadata

BASE_FILESHARE_URL = os.environ.get('FILESHARE_URL', 'https://geodata4edu.ethz.ch/metadata/')

WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

TRUE_VALUES = ['true', 'y', 'yes']


def _imported_entries():
    return GeoServiceMetadata.objects.filter(imported=True)


def _geovite_id(record_name):
    id = record_name.split('.')[0]
    return 'oai:geovite.ethz.ch:' + id


def _remove_duplicate_entries():
    to_be_deleted = []
    for record in _imported_entries():
        if _imported_entries().filter(identifier=record.identifier).count() > 1:
            to_be_deleted.append(_imported_entries().filter(identifier=record.identifier).exclude(api_id=record.api_id))
    for delete_em in to_be_deleted:
        delete_em.delete()


def _get_xml_file_names():
    page = requests.get(BASE_FILESHARE_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    for link in soup.find_all('a'):
        link_name = link.get('href')
        if link_name.endswith('.xml'):
            yield link_name


def read_xml(url):
    tree = ET.ElementTree(file=request.urlopen(BASE_FILESHARE_URL + url))
    root = tree.getroot()
    record = {}
    for child in root:
        content = child.text
        tag = child.tag.split('}', 1)[1]
        record[tag] = content
    record['login_name'] = 'GEOVITE_AUTOIMPORTER'
    record['is_latest'] = record.pop('publication_latest').lower() in TRUE_VALUES
    record['imported'] = True
    return record


def create_new_record(record_name, modified):
    data = read_xml(record_name)
    data['modified'] = modified
    data['identifier'] = _geovite_id(record_name)
    print('creating entry {}'.format(data['identifier']))
    GeoServiceMetadata.objects.create(**data)


def update_record(record, record_xml, modified):
    data = read_xml(record_xml)
    data['modified'] = modified
    _ = data.pop('identifier', None)
    print('updating entry {}'.format(record.identifier))
    _imported_entries().filter(api_id=record.api_id).update(**data)


def delete_obsolete_records(existing_record_identifiers):
    old_entries = _imported_entries().exclude(identifier__in=existing_record_identifiers)
    count = len(old_entries)
    print('removing {} entries'.format(count))
    old_entries.delete()


def update_entry(xml_file_name):
    last_modified = timezone.now()
    identifier = _geovite_id(xml_file_name)
    existing_record = _imported_entries().filter(identifier=identifier).first()
    if existing_record is not None:
        update_record(existing_record, xml_file_name, last_modified)
    else:
        create_new_record(xml_file_name, last_modified)
    return identifier


def update_harvested_records():
    existing_record_identifiers = []
    for xml_file_name in _get_xml_file_names():
        identifier = update_entry(xml_file_name)
        if identifier:
            existing_record_identifiers.append(identifier)
    delete_obsolete_records(existing_record_identifiers)


def harvest():
    _remove_duplicate_entries()
    update_harvested_records()
