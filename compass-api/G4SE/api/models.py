from __future__ import unicode_literals

from django.db import models


class Record(models.Model):
    identifier = models.CharField(primary_key=True, max_length=255)
    language = models.CharField(max_length=20)
    content = models.CharField(max_length=255)
    abstract = models.TextField()
    publication_year = models.IntegerField()
    publication_lineage = models.CharField(max_length=255, blank=True, null=True)
    geography = models.CharField(max_length=255)
    extent = models.CharField(max_length=255)
    geodata_type = models.CharField(max_length=255)
    source = models.CharField(max_length=2083)
    metadata_link = models.CharField(max_length=2083)
    access_link = models.CharField(max_length=2083)
    base_link = models.CharField(max_length=2083, blank=True, null=True)
    collection = models.CharField(max_length=255, blank=True, null=True)
    dataset = models.CharField(max_length=255, blank=True, null=True)
    arcgis_layer_link = models.CharField(max_length=2083, blank=True, null=True)
    qgis_layer_link = models.CharField(max_length=2083, blank=True, null=True)
    arcgis_symbology_link = models.CharField(max_length=2083, blank=True, null=True)
    qgis_symbology_link = models.CharField(max_length=2083, blank=True, null=True)
    service_type = models.CharField(max_length=255, blank=True, null=True)
    crs = models.CharField(max_length=20)
    term_link = models.CharField(max_length=2083)
    proved = models.DateField(blank=True, null=True)
    visibility = models.CharField(max_length=255)
    modified = models.DateTimeField(blank=True, null=True)
    login_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'records'

    def __str__(self):
        return self.content
