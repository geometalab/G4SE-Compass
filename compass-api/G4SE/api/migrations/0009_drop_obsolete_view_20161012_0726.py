# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-12 07:26
from __future__ import unicode_literals

from django.db import migrations


postgres_view_create = """
  CREATE OR REPLACE VIEW all_records AS
     SELECT records.extent::text AS extent, records.api_id, records.identifier, records.language, records.content, records.abstract, records.publication_year, records.publication_lineage, records.geography, records.geodata_type, records.source, records.metadata_link, records.access_link, records.base_link, records.collection, records.dataset, records.arcgis_layer_link, records.qgis_layer_link, records.arcgis_symbology_link, records.qgis_symbology_link, records.service_type, records.crs, records.term_link, records.proved, records.visibility, records.modified, records.login_name, records.search_vector_de, records.search_vector_en, records.search_vector_fr
       FROM records
    UNION
     SELECT harvested_records.extent::text AS extent, harvested_records.api_id, harvested_records.identifier, harvested_records.language, harvested_records.content, harvested_records.abstract, harvested_records.publication_year, harvested_records.publication_lineage, harvested_records.geography, harvested_records.geodata_type, harvested_records.source, harvested_records.metadata_link, harvested_records.access_link, harvested_records.base_link, harvested_records.collection, harvested_records.dataset, harvested_records.arcgis_layer_link, harvested_records.qgis_layer_link, harvested_records.arcgis_symbology_link, harvested_records.qgis_symbology_link, harvested_records.service_type, harvested_records.crs, harvested_records.term_link, harvested_records.proved, harvested_records.visibility, harvested_records.modified, harvested_records.login_name, harvested_records.search_vector_de, harvested_records.search_vector_en, harvested_records.search_vector_fr
       FROM harvested_records;
"""

postgres_view_drop = "DROP VIEW all_records;"

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_obsolete_triggers_20161011_1710'),
    ]

    operations = [
        migrations.RunSQL(postgres_view_drop, postgres_view_create)
    ]
