# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-12 09:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_NO_WAY_BACK_drop_obsolete_tables_20161012_0747'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadOnlyGeoServiceMetadata',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('api.geoservicemetadata',),
        ),
        migrations.AddField(
            model_name='geoservicemetadata',
            name='tags',
            field=models.ManyToManyField(through='api.GeoServiceMetadataTagItem', to='api.TranslationTag'),
        ),
    ]