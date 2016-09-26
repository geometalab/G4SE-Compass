import pytest

from api.models import CombinedRecord, Record, RecordTag, RecordTaggedItem
from api.views import StandardResultsSetPagination
from .testdata import data


@pytest.fixture
def tag(db):
    tag, _ = RecordTag.objects.get_or_create(
        tag_de='präzise', tag_en='house', tag_fr='maison'
    )
    assert RecordTaggedItem.objects.count() == 2
    return tag


def test_record_list(client, setup_database):
    record_list = client.get('/api/metadata/')
    assert len(record_list.data['results']) == StandardResultsSetPagination.page_size

    record_list = client.get('/api/metadata/?page_size=200')
    assert len(record_list.data['results']) == 21


def test_external_access(client, setup_database):
    record_list = client.get('/api/metadata/?page_size=200', REMOTE_ADDR="123.1.1.3")
    assert int(record_list.data['count']) == 20
    all_record_list = client.get('/api/metadata/')
    assert int(all_record_list.data['count']) == 21


def test_internal_record_detail(client, setup_database):
    record = client.get('/api/metadata/5e98dd86-e3c7-4a8b-895f-d555dde45566/')
    assert 'swissimage' in record.data.values()


def test_unauthorized_detail(client, setup_database):
    record = client.get('/api/metadata/5e98dd86-e3c7-4a8b-895f-d555dde45566/', REMOTE_ADDR="123.1.1.3")
    assert record.status_code == 403


def test_harvested_record_detail(client, setup_database):
    record = client.get('/api/metadata/17f17742-50d4-4882-94fb-3855922b0acc/')
    assert 'GeoVITe' in record.data.values()


def test_most_recent_records(client, admin_client, setup_database):
    record_list = client.get('/api/metadata/?ordering=-modified&limit=2')
    results = record_list.data['results']
    assert len(results) == 2

    # Add new record over API
    response = admin_client.post('/api/admin/', data, format='json')
    assert response.status_code == 201

    new_record_list = client.get('/api/metadata/?ordering=-modified&limit=2')
    new_record_list_results = new_record_list.data['results']

    assert len(new_record_list_results) == 2
    assert 'Topologisches Landschaftsmodell TLM, Fliessgewässer' in new_record_list_results[0].values()
    # cleanup
    Record.objects.filter(identifier=1234567).delete()


def test_search(client, setup_database):
    result_list = client.get('/api/metadata/?search=Zürich')
    for result in result_list.data['results']:
        assert 'Zürich' in result.values()


def test_external_search(client, setup_database):
    result = client.get('/api/metadata/?search=swissimage&language=de')
    assert len(result.data['results']) == 4
    external_result = client.get('/api/metadata/?search=swissimage', REMOTE_ADDR="123.1.1.3")
    assert len(external_result.data['results']) == 3


def test_or_search(client, setup_database):
    pipe = '%7C'
    result = client.get('/api/metadata/?search=orthophoto{}digital&language=de'.format(pipe))
    assert len(result.data['results']) == 17


def test_and_search(client, setup_database):
    ampersand = '%26'
    space = '%20'
    result = client.get('/api/metadata/?search=orthophoto{}digital&language=de'.format(ampersand))
    assert len(result.data['results']) == 4
    result = client.get('/api/metadata/?search=orthophoto{}digital&language=de'.format(space))
    assert len(result.data['results']) == 4
    result = client.get('/api/metadata/?search=orthophoto{}{}{}digital&language=de'.format(space, ampersand, space))
    assert len(result.data['results']) == 4


@pytest.mark.skipif(
    True,
    reason='This test currently is broken, since triggers are not being execute inside the transaction.'
)
def test_search_with_tags(setup_database, db, tag, client):
    pytest.set_trace()
    # ensure tag isn't matching
    result = client.get('/api/metadata/?search=house&language=de')
    assert result.status_code == 200
    assert len(result.data['results']) == 0

    # all should return the same
    result = client.get('/api/metadata/?search=präzis&language=de')
    assert result.status_code == 200
    assert len(result.data['results']) == 2

    result = client.get('/api/metadata/?search={}&language=en'.format(tag.tag_en))
    assert result.status_code == 200
    assert len(result.data['results']) == 2

    result = client.get('/api/metadata/?search=maison&language=fr')
    assert result.status_code == 200
    assert len(result.data['results']) == 2


def test_invalid_search_query(client, setup_database):
    result = client.get('/api/metadata/?search=orthophoto|%26digital&language=de')
    assert result.status_code == 400


def test_internal_records_list(admin_client, setup_database):
    result_list = admin_client.get('/api/admin/')
    assert len(result_list.data) == 10


def test_insert_record(client, admin_client, setup_database):
    records_before_insert = CombinedRecord.objects.all().count()
    admin_client.post('/api/admin/', data, format='json')
    assert CombinedRecord.objects.all().count() == records_before_insert + 1
    # Cleanup
    Record.objects.filter(identifier=1234567).delete()
