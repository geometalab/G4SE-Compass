from api.models import CombinedRecord, Record, HarvestedRecord


def test_all_records(setup_database):
    res = CombinedRecord.objects.all().count()
    assert res == 21


def test_record(setup_database):
    res = Record.objects.all().count()
    assert res == 10


def test_harvested_record(setup_database):
    res = HarvestedRecord.objects.all().count()
    assert res == 11
