from api.views import RecordList
from rest_framework.test import APITestCase
import pytest


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database')
class TestViews(APITestCase):

    def test_record_list(self):
        record_list = self.client.get('/api/')
        assert 'Schweiz' in record_list.data[0].values()
        assert 'Zürich' in record_list.data[3].values()

    def test_internal_record_detail(self):
        record = self.client.get('/api/123455/')
        assert 'Schweiz' in record.data.values()

    def test_harvested_record_detail(self):
        record = self.client.get('/api/12380/')
        assert 'Zürich' in record.data.values()

    def test_search(self):
        result_list = self.client.get('/api/search/?query=Zürich')
        assert 'Zürich' in result_list.data[0].values()

