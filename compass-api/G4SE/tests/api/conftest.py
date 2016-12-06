from django.db import connection, transaction
import pytest

from api.models import GeoServiceMetadata


def run_sql(path):
    f = open(path, "r")
    sql = f.read()
    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.atomic()


@pytest.fixture
def geo_service_metadata_base_kwargs():
    return {
        'identifier': '0',
        'language': GeoServiceMetadata.ENGLISH,
        'title': 'testentry',
        'abstract': 'some text in the entry',
        'publication_year': 2016,
        'publication_lineage': None,
        'is_latest': False,
        'geography': 'Schweiz',
        'geodata_type': GeoServiceMetadata.GEO_DATA_TYPE_RASTER,
        'source': 'http://example.com',
        'metadata_link': 'http://example.com',
        'access_link': 'http://example.com',
        'base_link': 'http://example.com',
        'collection': 'some collection',
        'dataset': None,
        'arcgis_layer_link': 'http://example.com',
        'qgis_layer_link': 'http://example.com',
        'arcgis_symbology_link': 'http://example.com',
        'qgis_symbology_link': 'http://example.com',
        'service_type': '',
        'crs': 'EPGS:4362',
        'term_link': 'http://example.com',
        'proved': None,
        'visibility': GeoServiceMetadata.VISIBILITY_PUBLIC,
        'login_name': 'test_login',
    }


def create_entry(**kwargs):
    metadata_kwargs = geo_service_metadata_base_kwargs().copy()
    metadata_kwargs.update(kwargs)
    return GeoServiceMetadata.objects.create(**metadata_kwargs)


@pytest.fixture
def imported_geo_service_metadata(db):
    entry = create_entry(**dict(imported=True))
    yield entry
    entry.delete()


@pytest.fixture
def editable_geo_service_metadata(db):
    entry = create_entry(**dict(imported=False))
    yield entry
    entry.delete()
