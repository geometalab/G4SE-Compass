import pytest
from api.models import CombinedRecord, Record
from .testdata import data
from api.views import Search


def test_record_list(client, setup_database):
    record_list = client.get('/api/metadata/')
    assert len(record_list.data) == 21


def test_external_access(client, setup_database):
    record_list = client.get('/api/metadata/', REMOTE_ADDR="123.1.1.3")
    assert len(record_list.data) == 20
    all_record_list = client.get('/api/metadata/')
    assert len(all_record_list.data) == 21


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
    record_list = client.get('/api/metadata/recent/?count=2')
    assert len(record_list.data) == 2

    # Add new record over API
    admin_client.post('/api/admin/create/', data, format='json')

    new_record_list = client.get('/api/metadata/recent/?count=2')
    assert len(record_list.data) == 2
    assert 'Topologisches Landschaftsmodell TLM, Fliessgewässer' in new_record_list.data[0].values()
    # cleanup
    Record.objects.filter(identifier=1234567).delete()


def test_parse_query(client, setup_database):
    and_query = Search.parse_query('A & B')
    assert and_query == 'A&B'
    or_query = Search.parse_query('A B')
    assert or_query == 'A|B'
    and_or_query = Search.parse_query('A & B C')
    assert and_or_query == 'A&B|C'
    multiple_whitespaces = Search.parse_query('A  &   B')
    assert multiple_whitespaces == 'A&B'


def test_parse_language(client, setup_database):
    german = Search.parse_language('de')
    assert german[0] == 'search_vector_de'
    assert german[1] == 'german'
    # Invalid Language should raise an error
    with pytest.raises(Exception) as exception_info:
        Search.parse_language('jibberish')


def test_search(client, setup_database):
    result_list = client.get('/api/metadata/search/?query=Zürich')
    for result in result_list.data:
        assert 'Zürich' in result.values()


def test_external_search(client, setup_database):
    result = client.get('/api/metadata/search/?query=swissimage&language=de')
    assert len(result.data) == 4
    empty_result = client.get('/api/metadata/search/?query=swissimage', REMOTE_ADDR="123.1.1.3")
    assert len(empty_result.data) == 3


def test_or_search(client, setup_database):
    result = client.get('/api/metadata/search/?query=orthofotho digital&language=de')
    assert len(result.data) == 17


def test_and_search(client, setup_database):
    result = client.get('/api/metadata/search/?query=orthophoto%26digital&language=de')
    assert len(result.data) == 4


def test_invalid_search_query(client, setup_database):
    result = client.get('/api/metadata/search/?query=orthophoto|%26digital&language=de')
    assert result.status_code == 400


def test_internal_records_list(admin_client, setup_database):
    result_list = admin_client.get('/api/admin/')
    assert len(result_list.data) == 10


def test_insert_record(client, admin_client, setup_database):
    records_before_insert = CombinedRecord.objects.all().count()
    admin_client.post('/api/admin/create/', data, format='json')
    assert CombinedRecord.objects.all().count() == records_before_insert + 1
    # Cleanup
    Record.objects.filter(identifier=1234567).delete()
