# -*- coding: utf-8 -*-
# Generated by Django 1.10.3.dev20161004124613 on 2016-10-10 12:53
from __future__ import unicode_literals

from django.db import migrations
from django.utils import timezone

from api.models import GEO_SERVICE_METADATA_AGREED_FIELDS


def _extract_publication_year(record_kwargs):
    if record_kwargs['publication_year'] == 'latest':
        record_kwargs['is_latest'] = True
        years = [int(year) for year in record_kwargs['publication_lineage'].split(',')]
        years.sort()
        record_kwargs['publication_year'] = years[-1]
    else:
        record_kwargs['publication_year'] = int(record_kwargs['publication_year'])
    return record_kwargs


def _normalize_kwargs(record_kwargs, record_object):
    record_kwargs['title'] = getattr(record_object, 'content')
    record_kwargs = _extract_publication_year(record_kwargs)
    return record_kwargs


def _extract_kwargs_(record_object, from_import):
    record_kwargs = {}
    fields = GEO_SERVICE_METADATA_AGREED_FIELDS.copy()
    fields.remove('is_latest')
    fields.remove('title')
    for field_name in fields:
        record_kwargs[field_name] = getattr(record_object, field_name)
    record_kwargs = _normalize_kwargs(record_kwargs, record_object)
    record_kwargs['imported'] = from_import
    if 'created' not in record_kwargs:
        record_kwargs['created'] = timezone.datetime(year=2016, month=9, day=30)
    return record_kwargs


def _create_new_entry(apps, model_kwargs):
    GeoServiceMetadata = apps.get_model("api", "GeoServiceMetadata")
    model_kwargs['geodata_type'] = model_kwargs['geodata_type'].lower()
    data_type = model_kwargs['geodata_type']
    if data_type not in ['raster', 'vector']:
        model_kwargs['geodata_type'] = 'other'
    GeoServiceMetadata.objects.create(**model_kwargs)


def forward(apps, schema_editor):
    # forward
    HarvestedRecord = apps.get_model("api", "HarvestedRecord")
    Record = apps.get_model("api", "Record")

    for harvested_record in HarvestedRecord.objects.all():
        _create_new_entry(apps, _extract_kwargs_(harvested_record, from_import=True))

    for record in Record.objects.all():
        _create_new_entry(apps, _extract_kwargs_(record, from_import=False))


def _kwargs_from_geo_service_metadata(geoservice_metadata_instance):
    result_kwargs = {}
    for field_name in GEO_SERVICE_METADATA_AGREED_FIELDS:
        result_kwargs[field_name] = getattr(geoservice_metadata_instance, field_name)
        result_kwargs['content'] = result_kwargs.pop('title')
    return result_kwargs


def backward(apps, schemap_editor):
    GeoServiceMetadata = apps.get_model("api", "GeoServiceMetadata")
    GeoServiceMetadata.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_geoservicemetadata'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
