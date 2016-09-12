from rest_framework.exceptions import ParseError
from rest_framework.test import APITestCase
import pytest
from django.contrib.auth.models import User
from api.models import AllRecords, Record
from .testdata import data
from api.views import Search


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database', 'test_user')
class TestListViews(APITestCase):

    def test_record_list(self):
        record_list = self.client.get('/api/metadata/')
        assert len(record_list.data) == 21

    def test_external_access(self):
        record_list = self.client.get('/api/metadata/', REMOTE_ADDR="123.1.1.3")
        assert len(record_list.data) == 20
        all_record_list = self.client.get('/api/metadata/')
        assert len(all_record_list.data) == 21

    def test_internal_record_detail(self):
        record = self.client.get('/api/metadata/5e98dd86-e3c7-4a8b-895f-d555dde45566/')
        assert 'swissimage' in record.data.values()

    def test_unauthorized_detail(self):
        record = self.client.get('/api/metadata/5e98dd86-e3c7-4a8b-895f-d555dde45566/', REMOTE_ADDR="123.1.1.3")
        assert record.status_code == 403

    def test_harvested_record_detail(self):
        record = self.client.get('/api/metadata/17f17742-50d4-4882-94fb-3855922b0acc/')
        assert 'GeoVITe' in record.data.values()

    def test_most_recent_records(self):
        record_list = self.client.get('/api/metadata/recent/?count=2')
        assert len(record_list.data) == 2

        # Add new record over API
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        self.client.post('/api/admin/create/', data, format='json')

        new_record_list = self.client.get('/api/metadata/recent/?count=2')
        assert len(record_list.data) == 2
        assert 'Topologisches Landschaftsmodell TLM, Fliessgewässer' in new_record_list.data[0].values()
        # cleanup
        Record.objects.filter(identifier=1234567).delete()


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database')
class TestSearchHelpers(APITestCase):

    def test_parse_query(self):
        and_query = Search.search_to_query_string('A & B')
        assert and_query == 'A&B'
        or_query = Search.search_to_query_string('A B')
        assert or_query == 'A|B'
        and_or_query = Search.search_to_query_string('A & B C')
        assert and_or_query == 'A&B|C'
        multiple_whitespaces = Search.search_to_query_string('A  &   B')
        assert multiple_whitespaces == 'A&B'


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database')
class TestSearchViews(APITestCase):

    def test_search(self):
        result_list = self.client.get('/api/metadata/search/?query=digital')
        assert len(result_list.data) > 0
        for result in result_list.data:
            assert any('digital' in value for value in result.values())

    def test_partial_word_search(self):
        result_list = self.client.get('/api/metadata/search/?query=digital')
        assert len(result_list.data) > 0
        for result in result_list.data:
            assert any('digital' in value for value in result.values())

    def test_external_search(self):
        result = self.client.get('/api/metadata/search/?query=swissimage&language=de')
        assert len(result.data) == 4
        empty_result = self.client.get('/api/metadata/search/?query=swissimage', REMOTE_ADDR="123.1.1.3")
        assert len(empty_result.data) == 3

    def test_or_search(self):
        result = self.client.get('/api/metadata/search/?query=orthofotho digital&language=de')
        assert len(result.data) == 17

    def test_and_search(self):
        result = self.client.get('/api/metadata/search/?query=orthophoto%26digital&language=de')
        assert len(result.data) == 4

    def test_invalid_search_query(self):
        result = self.client.get('/api/metadata/search/?query=orthophoto|%26digital&language=de')
        assert result.status_code == 400


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database', 'test_user')
class TestAuthentication(APITestCase):

    def test_authenticate(self):
        assert self.client.login(username='admin', password='securepassword')
        self.client.logout()
        assert self.client.login(username='admin', password='wrongpassword') is False


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database', 'test_user')
class TestBackendViews(APITestCase):

    def test_internal_records_list(self):
        self.client.login(username='admin', password='securepassword')
        result_list = self.client.get('/api/admin/')
        assert len(result_list.data) == 10

    def test_insert_record(self):
        records_before_insert = AllRecords.objects.all().count()
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        self.client.post('/api/admin/create/', data, format='json')
        assert AllRecords.objects.all().count() == records_before_insert + 1
        # Cleanup
        Record.objects.filter(identifier=1234567).delete()
