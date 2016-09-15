from __future__ import unicode_literals
import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.utils.translation import ugettext_lazy as _


class Base(models.Model):
    """
    Abstract base model for G4SE metadata records
    """
    api_id = models.CharField(primary_key=True, max_length=100, editable=False, default=uuid.uuid4)
    identifier = models.CharField(max_length=255)
    GERMAN = 'de'
    FRENCH = 'fr'
    ENGLISH = 'en'
    # Enums for language
    language_choices = (
        (GERMAN, 'de'),
        (FRENCH, 'fr'),
        (ENGLISH, 'en'),
    )
    language = models.CharField(max_length=20, choices=language_choices, default=GERMAN)
    content = models.CharField(max_length=255)
    abstract = models.TextField()
    publication_year = models.CharField(max_length=20)
    publication_lineage = models.CharField(max_length=255, blank=True, null=True)
    geography = models.CharField(max_length=255)
    extent = models.CharField(max_length=255, null=True)
    geodata_type = models.CharField(max_length=255)
    source = models.CharField(max_length=2083)
    metadata_link = models.URLField(max_length=2083)
    access_link = models.URLField(max_length=2083)
    base_link = models.URLField(max_length=2083, blank=True, null=True)
    collection = models.CharField(max_length=255, blank=True, null=True)
    dataset = models.CharField(max_length=255, blank=True, null=True)
    arcgis_layer_link = models.URLField(max_length=2083, blank=True, null=True)
    qgis_layer_link = models.URLField(max_length=2083, blank=True, null=True)
    arcgis_symbology_link = models.URLField(max_length=2083, blank=True, null=True)
    qgis_symbology_link = models.URLField(max_length=2083, blank=True, null=True)
    service_type = models.CharField(max_length=255, blank=True, null=True)
    crs = models.CharField(max_length=20)
    term_link = models.URLField(max_length=2083)
    proved = models.DateField(blank=True, null=True)
    # Enums for visibility
    PUBLIC = 'public'
    TEST = 'test'
    HSR_INTERNAL = 'hsr-internal'
    visibility_choices = (
        (PUBLIC, 'public'),
        (TEST, 'test'),
        (HSR_INTERNAL, 'hsr-internal'),
    )
    visibility = models.CharField(max_length=255, choices=visibility_choices, default=PUBLIC)
    modified = models.DateTimeField(blank=True, null=True)
    login_name = models.CharField(max_length=255, blank=True, null=True)
    search_vector_de = SearchVectorField()
    search_vector_en = SearchVectorField()
    search_vector_fr = SearchVectorField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.content


class CombinedRecord(Base):
    """
    Model to represent database view witch unions the record and harvested_record table
    """
    class Meta:
        managed = False
        db_table = 'all_records'


class Record(Base):
    """
    Model for data edited in G4SE directly
    """
    class Meta:
        managed = False
        db_table = 'records'


class HarvestedRecord(Base):
    """
    Model for harvested metadata records
    """
    class Meta:
        managed = False
        db_table = 'harvested_records'


class RecordTag(models.Model):
    """
    A single tag with language associations
    """
    LANGUAGE_DE = 'de'
    LANGUAGE_EN = 'en'
    LANGUAGE_FR = 'fr'
    LANGUAGE_CHOICES = (
        (LANGUAGE_EN, _(LANGUAGE_EN)),
        (LANGUAGE_DE, _(LANGUAGE_DE)),
        (LANGUAGE_FR, _(LANGUAGE_FR)),
    )
    tag_de = models.CharField(_('tag de'), max_length=200)
    tag_en = models.CharField(_('tag en'), max_length=200)
    tag_fr = models.CharField(_('tag fr'), max_length=200)

    tag_alternative_de = ArrayField(
        models.CharField(max_length=200, blank=True),
        help_text=_('comma separated extra fields'),
    )
    tag_alternative_en = ArrayField(
        models.CharField(max_length=200, blank=True),
        help_text=_('comma separated extra fields'),
    )
    tag_alternative_fr = ArrayField(
        models.CharField(max_length=200, blank=True),
        help_text=_('comma separated extra fields'),
    )

    tag_de_search_vector = SearchVectorField()
    tag_en_search_vector = SearchVectorField()
    tag_fr_search_vector = SearchVectorField()

    # since CombinedRecord is not a table we need to use generic foreignkey...
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=100)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "{}/{}/{}".format(self.tag_de, self.tag_en, self.tag_fr)

    class Meta:
        db_table = 'record_tag'
