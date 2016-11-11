# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 10:04
from __future__ import unicode_literals

from django.db import migrations, models


def use_none_for_not_imported(apps, schema_editor):
    GeoServiceMetadata = apps.get_model("api", "GeoServiceMetadata")
    for md in GeoServiceMetadata.objects.filter(imported=False, is_latest=False):
        md.is_latest = None
        md.save()


def none_to_false(apps, schema_editor):
    GeoServiceMetadata = apps.get_model("api", "GeoServiceMetadata")
    for md in GeoServiceMetadata.objects.filter(imported=False, is_latest__isnull=True):
        md.is_latest = False
        md.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20161014_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geoservicemetadata',
            name='is_latest',
            field=models.NullBooleanField(default=None, verbose_name='latest of series'),
        ),
        migrations.RunPython(use_none_for_not_imported, none_to_false),
    ]