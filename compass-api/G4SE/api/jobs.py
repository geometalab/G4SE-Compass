import os
import tempfile
import zipfile

import django_rq

from api.geovite_importer import import_records
from api.models import GeoVITeImportData


def extract_xml_paths(zip_file, directory):
    paths = []
    for file_name in zip_file.namelist():
        if file_name.endswith('.xml'):
            paths.append(os.path.dirname(os.path.join(directory, file_name)))
            zip_file.extract(file_name, path=directory)
    return set(paths)


def import_zipped_xml(instance_id):
    geovite_importer_instance = GeoVITeImportData.objects.get(id=instance_id)
    if not geovite_importer_instance.is_imported:
        xml_zip_path = geovite_importer_instance.xml_zip.path
        with tempfile.TemporaryDirectory() as temp_dir:
            geovite_zip = zipfile.ZipFile(xml_zip_path)
            for path in extract_xml_paths(geovite_zip, temp_dir):
                import_records(path)
        geovite_importer_instance.is_imported = True
        geovite_importer_instance.save()


def delayed_xml_zip_import(sender, instance, **_):
    django_rq.enqueue(import_zipped_xml, instance_id=instance.id)
