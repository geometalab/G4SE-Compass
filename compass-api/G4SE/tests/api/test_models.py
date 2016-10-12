from api.models import GeoServiceMetadata


def test_all_records(editable_geo_service_metadata, imported_geo_service_metadata):
    res = GeoServiceMetadata.objects.all().count()
    assert res == 2
    res = GeoServiceMetadata.objects.filter(imported=False).count()
    assert res == 1
    res = GeoServiceMetadata.objects.filter(imported=True).count()
    assert res == 1
