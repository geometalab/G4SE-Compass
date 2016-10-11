from __future__ import unicode_literals
import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.utils.translation import ugettext_lazy as _

from api import LANGUAGE_CONFIG_MATCH
from api.search_parser import search_query_parser
from api.search_parser.query_parser import SearchSemantics


class Base(models.Model):
    """
    Abstract base model for G4SE metadata records
    """
    api_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
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
    extent = models.CharField(max_length=255, null=True, blank=True, help_text='needs follow the form `BOX(0 0,1 1)`')
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

    @property
    def tags(self):
        return RecordTaggedItem.objects.filter(object_id=self.api_id).order_by('id')

    @property
    def tags_de(self):
        tags = []
        for tag in self.tags:
            tags += tag.all_tag_list(self.GERMAN)
        return tags

    @property
    def tags_en(self):
        tags = []
        for tag in self.tags:
            tags += tag.all_tag_list(self.ENGLISH)
        return tags

    @property
    def tags_fr(self):
        tags = []
        for tag in RecordTaggedItem.objects.filter(object_id=self.api_id).order_by('id'):
            tags += tag.all_tag_list(self.FRENCH)
        return tags

    def tag_list_display(self):
        tags = self.tags
        if len(tags) > 0:
            return ', '.join([str(t) for t in tags])
        return ' - '
    tag_list_display.short_description = 'tags'

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


class RecordTaggedItem(models.Model):
    # since CombinedRecord is not a table we need to use generic foreignkey...
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    record_tag = models.ForeignKey('RecordTag')

    def all_tag_list(self, language):
        main_tag = getattr(self.record_tag, 'tag_{}'.format(language))
        translations = getattr(self.record_tag, 'tag_alternatives_{}'.format(language))
        return [main_tag] + translations

    def __str__(self):
        return "{}/{}/{}".format(self.record_tag.tag_de, self.record_tag.tag_en, self.record_tag.tag_fr)


class RecordTag(models.Model):
    """
    A single tag with language associations
    """
    tag_de = models.CharField(_('tag de'), max_length=200, unique=True)
    tag_en = models.CharField(_('tag en'), max_length=200, unique=True)
    tag_fr = models.CharField(_('tag fr'), max_length=200, unique=True)

    tag_alternatives_de = ArrayField(
        models.CharField(max_length=200),
        blank=True,
        null=True,
        help_text=_('comma separated extra fields'),

    )
    tag_alternatives_en = ArrayField(
        models.CharField(max_length=200),
        blank=True,
        null=True,
        help_text=_('comma separated extra fields'),
    )
    tag_alternatives_fr = ArrayField(
        models.CharField(max_length=200),
        blank=True,
        null=True,
        help_text=_('comma separated extra fields'),
    )

    tag_de_search_vector = SearchVectorField(blank=True, null=True)
    tag_en_search_vector = SearchVectorField(blank=True, null=True)
    tag_fr_search_vector = SearchVectorField(blank=True, null=True)

    def __str__(self):
        return "{}/{}/{}".format(self.tag_de, self.tag_en, self.tag_fr)

    class Meta:
        db_table = 'record_tag'


def record_ids_for_search_query(search_query, language='de'):
    if isinstance(search_query, str):
        language_for_pg = LANGUAGE_CONFIG_MATCH[language]
        search_query = search_query_parser.UnknownParser().parse(
            search_query,
            semantics=SearchSemantics(config=language_for_pg)
        )
    vector = 'tag_{}_search_vector'.format(language)
    search_kwargs = {
        vector: search_query
    }
    tags = RecordTag.objects.filter(**search_kwargs)
    return RecordTaggedItem.objects.filter(
        record_tag__in=tags
    ).values_list('object_id', flat=True)


class GeoServiceMetadata(models.Model):
    """
    G4SE Geografic Services' metadata
    """
    GERMAN = 'de'
    FRENCH = 'fr'
    ENGLISH = 'en'

    LANGUAGE_CHOICES = (
        (GERMAN, _('de')),
        (FRENCH, _('fr')),
        (ENGLISH, _('en')),
    )

    VISIBILITY_PUBLIC = 'public'
    VISIBILITY_TEST = 'test'
    VISIBILITY_HSR_INTERNAL = 'hsr-internal'
    VISIBILITY_CHOICES = (
        (VISIBILITY_PUBLIC, _('public')),
        (VISIBILITY_TEST, _('test')),
        (VISIBILITY_HSR_INTERNAL, _('hsr-internal')),
    )

    GEO_DATA_TYPE_RASTER = 'raster'
    GEO_DATA_TYPE_VECTOR = 'vector'
    GEO_DATA_TYPES = (
        (GEO_DATA_TYPE_RASTER, _('raster')),
        (GEO_DATA_TYPE_VECTOR, _('vector')),
    )

    api_id = models.UUIDField(_('uuid'), primary_key=True, editable=False, default=uuid.uuid4)
    identifier = models.CharField(_('external identifier'), max_length=255)
    language = models.CharField(_('language'), max_length=20, choices=LANGUAGE_CHOICES, default=GERMAN)
    title = models.CharField(_('title'), max_length=255)
    abstract = models.TextField(_('abstract'))
    publication_year = models.IntegerField(_('publication year'))
    publication_lineage = models.CharField(_('history'), max_length=255, blank=True, null=True)
    is_latest = models.BooleanField(_('latest of series'), max_length=255, default=False)
    geography = models.CharField(_('geography'), max_length=255, default='Schweiz')
    extent = models.CharField(
        _('extent'), max_length=255, null=True, blank=True, help_text='needs follow the form `BOX(x1 y1,x2 y2)`'
    )
    geodata_type = models.CharField(_('geodata type'), max_length=255, choices=GEO_DATA_TYPES)
    source = models.CharField(_('source'), max_length=2083)
    metadata_link = models.URLField(_('metadata link'), max_length=2083)
    access_link = models.URLField(_('access link'), max_length=2083)
    base_link = models.URLField(_('access to data'), max_length=2083, blank=True, null=True)
    collection = models.CharField(_('group name'), max_length=255, blank=True, null=True)
    dataset = models.CharField(_('dataset name'), max_length=255, blank=True, null=True)
    arcgis_layer_link = models.URLField(_('ArcGIS layer link'), max_length=2083, blank=True, null=True)
    qgis_layer_link = models.URLField(_('QGIS layer link'), max_length=2083, blank=True, null=True)
    arcgis_symbology_link = models.URLField(_('ArcGIS symbology link'), max_length=2083, blank=True, null=True)
    qgis_symbology_link = models.URLField(_('QGIS symbology link'), max_length=2083, blank=True, null=True)
    service_type = models.CharField(_('service type'), max_length=255, blank=True, null=True)
    crs = models.CharField(_('coordinate reference system'), max_length=20)
    term_link = models.URLField(_('terms of use'), max_length=2083)
    proved = models.DateField(_('proving date'), blank=True, null=True)
    visibility = models.CharField(
        _('access restriction'), max_length=255, choices=VISIBILITY_CHOICES, default=VISIBILITY_PUBLIC
    )
    login_name = models.CharField(_('login name'), max_length=255)

    modified = models.DateTimeField(_('last modification'), auto_now=True, blank=True, null=True)
    created = models.DateTimeField(_('created on'), auto_now_add=True)
    imported = models.BooleanField(_('imported'), editable=False, default=False)

    @property
    def tags(self):
        return RecordTaggedItem.objects.filter(object_id=self.api_id).order_by('id')

    @property
    def tags_de(self):
        tags = []
        for tag in self.tags:
            tags += tag.all_tag_list(self.GERMAN)
        return tags

    @property
    def tags_en(self):
        tags = []
        for tag in self.tags:
            tags += tag.all_tag_list(self.ENGLISH)
        return tags

    @property
    def tags_fr(self):
        tags = []
        for tag in RecordTaggedItem.objects.filter(object_id=self.api_id).order_by('id'):
            tags += tag.all_tag_list(self.FRENCH)
        return tags

    def tag_list_display(self):
        tags = self.tags
        if len(tags) > 0:
            return ', '.join([str(t) for t in tags])
        return ' - '
    tag_list_display.short_description = 'tags'

    def __str__(self):
        return self.content
