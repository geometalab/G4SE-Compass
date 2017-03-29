import pytest

from api.models import TranslationTag, GeoServiceMetadata, GeoServiceMetadataTagItem
from tests.api.conftest import create_entry


@pytest.fixture
def precreated_geo_service_metadata(db, request):
    entries = [
        create_entry(**dict(
            language=GeoServiceMetadata.ENGLISH,
            title='house',
            abstract='Some content',
        )),
        create_entry(**dict(
            language=GeoServiceMetadata.GERMAN,
            title='präzise',
            abstract='Inhalt',
        )),
        create_entry(**dict(
            language=GeoServiceMetadata.GERMAN,
            title='digital',
            abstract='digital sagitarius orthophoto',
        )),
        create_entry(**dict(
            language=GeoServiceMetadata.GERMAN,
            title='Omnivor',
            abstract='Digital and other stuff orthophoto',
            imported=True,
        )),
        create_entry(**dict(
            language=GeoServiceMetadata.GERMAN,
            title='asdad ad',
            abstract='other stuff orthophoto',
        )),
        create_entry(**dict(
            language=GeoServiceMetadata.GERMAN,
            title='asölkdsjlökadj',
            abstract='kein hamster überlebte',
            visibility=GeoServiceMetadata.VISIBILITY_HSR_INTERNAL,
        ))
    ]
    yield entries
    for entry in entries:
        entry.delete()


@pytest.fixture
def tag(db, precreated_geo_service_metadata):
    tag, _ = TranslationTag.objects.get_or_create(
        tag_de='präzise', tag_en='house', tag_fr='maison'
    )
    assert GeoServiceMetadataTagItem.objects.count() == 2
    return tag


def test_record_list(client, precreated_geo_service_metadata):
    record_list = client.get('/api/search/?page_size=200')
    assert len(record_list.data['results']) == 6


def test_external_access(client, precreated_geo_service_metadata):
    record_list = client.get('/api/metadata/?page_size=200', REMOTE_ADDR='123.1.1.1')
    assert int(record_list.data['count']) == 5
    all_record_list = client.get('/api/metadata/?visibility={},{}'.format(
        GeoServiceMetadata.VISIBILITY_HSR_INTERNAL,
        GeoServiceMetadata.VISIBILITY_PUBLIC,
    ))
    assert int(all_record_list.data['count']) == 6


def test_external_search(client, precreated_geo_service_metadata):
    result = client.get('/api/search/?language=de', REMOTE_ADDR='123.1.1.1')
    assert result.status_code == 200
    assert len(result.data['results']) == 5
    external_result = client.get('/api/search/?language=de')
    assert len(external_result.data['results']) == 6


def test_or_search(client, precreated_geo_service_metadata):
    pipe = '%20OR%20'
    result = client.get('/api/search/?search=orthophoto{}digital&language=de'.format(pipe))
    assert len(result.data['results']) == 3


def test_and_search(client, precreated_geo_service_metadata):
    AND = '%20AND%20'
    space = '%20'
    result = client.get('/api/search/?search=orthophoto{}digital&language=de'.format(AND))
    assert len(result.data['results']) == 2
    result = client.get('/api/search/?search=orthophoto{}digital&language=de'.format(space))
    assert len(result.data['results']) == 2
    result = client.get('/api/search/?search=orthophoto{}{}{}digital&language=de'.format(space, AND, space))
    assert len(result.data['results']) == 2


def test_internal_records_list(admin_client, precreated_geo_service_metadata):
    result_list = admin_client.get('/api/admin/')
    assert len(result_list.data['results']) == 5


def test_invalid_search_query(client, precreated_geo_service_metadata):
    # just ignore characters
    result = client.get('/api/search/?search=orthophoto)(digital&language=de')
    assert result.status_code == 200
