import xml.etree.ElementTree as ET

from django.utils import timezone
import os

from api.models import GeoServiceMetadata

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
            to_be_deleted.append(_imported_entries().filter(identifier=record.identifier).exclude(api_id=record.api_id))  # noqa: line too long
    for delete_em in to_be_deleted:
        delete_em.delete()


def _get_xml_files(path):
    for file_name in os.listdir(path):
        if file_name.endswith(".xml"):
            yield os.path.join(path, file_name)


def read_xml(file_path, identifier):
    tree = ET.parse(file_path)
    root = tree.getroot()
    record = {}
    for child in root:
        content = child.text
        tag = child.tag.split('}', 1)[1]
        record[tag] = content
    record['login_name'] = 'GEOVITE_AUTOIMPORTER'
    record['is_latest'] = record.pop('publication_latest').lower() in TRUE_VALUES
    record['imported'] = True
    record['identifier'] = identifier
    record['modified'] = timezone.now()
    return record


def delete_obsolete_records(existing_record_identifiers):
    old_entries = _imported_entries().exclude(identifier__in=existing_record_identifiers)
    count = len(old_entries)
    print('removing {} entries'.format(count))
    old_entries.delete()


def _import_record(xml_file_path, identifier):
    data = read_xml(xml_file_path, identifier)
    existing = GeoServiceMetadata.objects.filter(identifier=identifier)
    if existing.count() > 0:
        print('updating {}'.format(identifier))
        data.pop('identifier')
        existing.update(**data)
    else:
        print('creating {}'.format(identifier))
        GeoServiceMetadata.objects.create(**data)


def import_records(base_path):
    _remove_duplicate_entries()
    existing_record_identifiers = []
    for xml_file_path in _get_xml_files(base_path):
        xml_base_name = os.path.basename(xml_file_path)
        identifier = _geovite_id(xml_base_name)
        _import_record(xml_file_path, identifier)
        existing_record_identifiers.append(identifier)
    delete_obsolete_records(existing_record_identifiers)
