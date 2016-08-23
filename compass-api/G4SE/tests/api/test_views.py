from rest_framework.test import APITestCase
import pytest
from django.contrib.auth.models import User
from api.models import AllRecords, Record
from .testdata import data


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database', 'test_user')
class TestListViews(APITestCase):

    def test_record_list(self):
        record_list = self.client.get('/api/')
        assert 'Schweiz' in record_list.data[0].values()
        assert 'Zürich' in record_list.data[2].values()

    def test_external_access(self):
        record_list = self.client.get('/api/', REMOTE_ADDR="123.1.1.3")
        assert len(record_list.data) == 2
        all_record_list = self.client.get('/api/')
        assert len(all_record_list.data) == 3

    def test_internal_record_detail(self):
        record = self.client.get('/api/5e9c6175-ead7-4637-af93-ec28a9d28f8a/')
        assert 'Schweiz' in record.data.values()

    def test_unauthorized_detail(self):
        record = self.client.get('/api/5e9c6175-ead7-4637-af93-ec28a9d28f8a/', REMOTE_ADDR="123.1.1.3")
        assert record.status_code == 403

    def test_harvested_record_detail(self):
        record = self.client.get('/api/dcb9cfe2-4568-4c30-971f-a4103d6e0ee9/')
        assert 'Zürich' in record.data.values()

    def test_most_recent_records(self):
        record_list = self.client.get('/api/recent/?count=2')
        assert len(record_list.data) == 2

        # Add new record over API
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        self.client.post('/api/admin/create/', data, format='json')

        new_record_list = self.client.get('/api/recent/?count=2')
        assert len(record_list.data) == 2
        assert 'Topologisches Landschaftsmodell TLM, Fliessgewässer' in new_record_list.data[0].values()
        # cleanup
        Record.objects.filter(identifier=1234567).delete()


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database')
class TestSearchViews(APITestCase):

    def test_search(self):
        result_list = self.client.get('/api/search/?query=Zürich')
        for result in result_list.data:
            assert 'Zürich' in result.values()

    def test_external_search(self):
        result = self.client.get('/api/search/?query=Landschaftsmodell')
        assert len(result.data) == 1
        empty_result = self.client.get('/api/search/?query=Landschaftsmodell', REMOTE_ADDR="123.1.1.3")
        assert len(empty_result.data) == 0


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database', 'test_user')
class TestAuthentication(APITestCase):

    def test_authenticate(self):
        assert self.client.login(username='admin', password='securepassword')
        self.client.logout()
        assert self.client.login(username='admin', password='wrongpassword') == False


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database', 'test_user')
class TestBackendViews(APITestCase):

    def test_internal_records_list(self):
        self.client.login(username='admin', password='securepassword')
        result_list = self.client.get('/api/admin/')
        assert len(result_list.data) == 2

    def test_insert_record(self):
        records_before_insert = AllRecords.objects.all().count()
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        self.client.post('/api/admin/create/', data, format='json')
        assert AllRecords.objects.all().count() == records_before_insert + 1
        # Cleanup
        Record.objects.filter(identifier=1234567).delete()
