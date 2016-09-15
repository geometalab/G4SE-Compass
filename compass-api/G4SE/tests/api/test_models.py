from api.models import CombinedRecord, Record, HarvestedRecord
import pytest


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database')
class TestModels:

    def test_all_records(self):
        res = CombinedRecord.objects.all().count()
        assert res == 21

    def test_record(self):
        res = Record.objects.all().count()
        assert res == 10

    def test_harvested_record(self):
        res = HarvestedRecord.objects.all().count()
        assert res == 11
