# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 06:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_geoviteimportdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geoviteimportdata',
            name='in_use',
        ),
        migrations.AddField(
            model_name='geoviteimportdata',
            name='is_imported',
            field=models.BooleanField(default=False, help_text='has this data been imported', verbose_name='imported'),
        ),
    ]