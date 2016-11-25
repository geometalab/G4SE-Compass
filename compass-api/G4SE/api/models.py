from __future__ import unicode_literals

import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _


class GeoServiceMetadataTagItem(models.Model):
    geo_service_metadata = models.ForeignKey('GeoServiceMetadata')
    tag = models.ForeignKey('TranslationTag')

    def __str__(self):
        return "{}/{}/{}".format(self.tag.tag_de, self.tag.tag_en, self.tag.tag_fr)


class TranslationTag(models.Model):
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

    def tags_for_language(self, language):
        main_tag = getattr(self, 'tag_{}'.format(language))
        translations = getattr(self, 'tag_alternatives_{}'.format(language))
        return [main_tag] + translations

    def __str__(self):
        return "{}/{}/{}".format(self.tag_de, self.tag_en, self.tag_fr)


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
    GEO_DATA_TYPE_OTHER = 'other'
    GEO_DATA_TYPES = (
        (GEO_DATA_TYPE_RASTER, _('raster')),
        (GEO_DATA_TYPE_VECTOR, _('vector')),
        (GEO_DATA_TYPE_OTHER, _('other')),
    )

    api_id = models.UUIDField(_('uuid'), primary_key=True, editable=False, default=uuid.uuid4)
    identifier = models.CharField(_('external identifier'), max_length=255)
    language = models.CharField(_('language'), max_length=20, choices=LANGUAGE_CHOICES, default=GERMAN)
    title = models.CharField(_('title'), max_length=255)
    abstract = models.TextField(_('abstract'))
    publication_year = models.IntegerField(_('publication year'))
    publication_lineage = models.TextField(_('history'), blank=True, null=True)
    is_latest = models.NullBooleanField(_('latest of series'), default=None)
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

    tags = models.ManyToManyField(TranslationTag, through='GeoServiceMetadataTagItem')

    @property
    def tags_de(self):
        tags = []
        for tag in self.tags.all():
            tags += tag.tags_for_language(self.GERMAN)
        return tags

    @property
    def tags_en(self):
        tags = []
        for tag in self.tags.all():
            tags += tag.tags_for_language(self.ENGLISH)
        return tags

    @property
    def tags_fr(self):
        tags = []
        for tag in self.tags.all():
            tags += tag.tags_for_language(self.FRENCH)
        return tags

    def tag_list_display(self):
        tags = self.tags.all()
        if len(tags) > 0:
            return ', '.join([str(t) for t in tags])
        return ' - '
    tag_list_display.short_description = 'tags'

    def __str__(self):
        return self.title


class GeoVITeImportData(models.Model):
    xml_zip = models.FileField(_('zipped GeoVite XML files'), help_text=_('not existing files will be deleted'))
    modified = models.DateTimeField(_('last modification'), auto_now=True, blank=True, null=True)
    created = models.DateTimeField(_('created on'), auto_now_add=True)
    is_imported = models.BooleanField(
        _('imported'), help_text=_('has this data been imported'), default=False
    )

    def __str__(self):
        return 'from {}'.format(self.created)


GEO_SERVICE_METADATA_AGREED_FIELDS = [
    'api_id',
    'identifier',
    'language',
    'title',
    'abstract',
    'publication_year',
    'publication_lineage',
    'is_latest',
    'geography',
    'geodata_type',
    'source',
    'metadata_link',
    'access_link',
    'base_link',
    'collection',
    'dataset',
    'arcgis_layer_link',
    'qgis_layer_link',
    'arcgis_symbology_link',
    'qgis_symbology_link',
    'service_type',
    'crs',
    'term_link',
    'proved',
    'visibility',
    'login_name',
    'modified',
]
