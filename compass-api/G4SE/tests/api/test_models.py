from api.models import AllRecords, Record, HarvestedRecord
import pytest


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database')
class TestModels:

    def test_all_records(self):
        res = AllRecords.objects.all().count()
        assert res == 3

    def test_record(self):
        res = Record.objects.all().count()
        assert res == 2

    def test_harvested_record(self):
        res = HarvestedRecord.objects.all().count()
        assert res == 1
