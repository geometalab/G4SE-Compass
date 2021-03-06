# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 13:10
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion

create_update_tsv_function = """
CREATE OR REPLACE FUNCTION {function_name}()
RETURNS TRIGGER AS $$
BEGIN
    NEW.tag_{lang}_search_vector := to_tsvector('pg_catalog.{pg_lang}', array_to_string(NEW.tag_alternatives_{lang}, ' ')) ||
    to_tsvector('pg_catalog.{pg_lang}', NEW.tag_{lang});
    RETURN NEW;
END;
$$ language 'plpgsql';
"""

add_trigger = """
CREATE TRIGGER {trigger_name} BEFORE INSERT OR UPDATE
    ON {table} FOR EACH ROW EXECUTE PROCEDURE {function_name}();
"""


remove_trigger = """
DROP TRIGGER IF EXISTS {trigger_name} ON {table};
"""

remove_function = """
DROP FUNCTION IF EXISTS {function_name}();
"""

FUNCTION_BASE_NAME = 'tsvector_update_'
TRIGGER_BASE_NAME = 'tsvector_trigger_'


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('api', '0002_allrecords_harvestedrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_de', models.CharField(max_length=200, unique=True, verbose_name='tag de')),
                ('tag_en', models.CharField(max_length=200, unique=True, verbose_name='tag en')),
                ('tag_fr', models.CharField(max_length=200, unique=True, verbose_name='tag fr')),
                ('tag_alternatives_de', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, help_text='comma separated extra fields', null=True, size=None)),
                ('tag_alternatives_en', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, help_text='comma separated extra fields', null=True, size=None)),
                ('tag_alternatives_fr', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, help_text='comma separated extra fields', null=True, size=None)),
                ('tag_de_search_vector', django.contrib.postgres.search.SearchVectorField(blank=True, null=True)),
                ('tag_en_search_vector', django.contrib.postgres.search.SearchVectorField(blank=True, null=True)),
                ('tag_fr_search_vector', django.contrib.postgres.search.SearchVectorField(blank=True, null=True)),
            ],
            options={
                'db_table': 'record_tag',
            },
        ),
        migrations.CreateModel(
            name='RecordTaggedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField()),
                ('content_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.AddField(
            model_name='recordtaggeditem',
            name='record_tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.RecordTag'),
        ),
        migrations.RunSQL(
            [
                (create_update_tsv_function.format(trigger_name=TRIGGER_BASE_NAME + 'tag_de', table='record_tag',
                                                   function_name=FUNCTION_BASE_NAME + 'tag_de', pg_lang='german',
                                                   lang='de')),
                (create_update_tsv_function.format(trigger_name=TRIGGER_BASE_NAME + 'tag_en', table='record_tag',
                                                   function_name=FUNCTION_BASE_NAME + 'tag_en', pg_lang='english',
                                                   lang='en')),
                (create_update_tsv_function.format(trigger_name=TRIGGER_BASE_NAME + 'tag_fr', table='record_tag',
                                                   function_name=FUNCTION_BASE_NAME + 'tag_fr', pg_lang='french',
                                                   lang='fr')),
                (remove_trigger.format(trigger_name=TRIGGER_BASE_NAME + 'tag_de', table='record_tag')),
                (remove_trigger.format(trigger_name=TRIGGER_BASE_NAME + 'tag_en', table='record_tag')),
                (remove_trigger.format(trigger_name=TRIGGER_BASE_NAME + 'tag_fr', table='record_tag')),
                (add_trigger.format(trigger_name=TRIGGER_BASE_NAME + 'tag_de', table='record_tag',
                                    function_name=FUNCTION_BASE_NAME + 'tag_de')),
                (add_trigger.format(trigger_name=TRIGGER_BASE_NAME + 'tag_en', table='record_tag',
                                    function_name=FUNCTION_BASE_NAME + 'tag_en')),
                (add_trigger.format(trigger_name=TRIGGER_BASE_NAME + 'tag_fr', table='record_tag',
                                    function_name=FUNCTION_BASE_NAME + 'tag_fr')),
            ],
            [
                (remove_trigger.format(trigger_name=TRIGGER_BASE_NAME + 'tag_de', table='record_tag')),
                (remove_trigger.format(trigger_name=TRIGGER_BASE_NAME + 'tag_en', table='record_tag')),
                (remove_trigger.format(trigger_name=TRIGGER_BASE_NAME + 'tag_fr', table='record_tag')),
                (remove_function.format(function_name=FUNCTION_BASE_NAME + 'tag_de')),
                (remove_function.format(function_name=FUNCTION_BASE_NAME + 'tag_en')),
                (remove_function.format(function_name=FUNCTION_BASE_NAME + 'tag_fr')),
            ],

        )
    ]
