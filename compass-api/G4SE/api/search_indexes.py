from haystack import indexes
from haystack.fields import DateTimeField, IntegerField, BooleanField

from configurable_elastic_search_backend import fields

from api.models import GeoServiceMetadata


class GeoServiceMetadataIndex(indexes.SearchIndex, indexes.Indexable):
    text = fields.CharField(document=True, use_template=True, analyzer='english_stemmer')
    api_id = fields.CharField(model_attr="api_id", boost=0.1)
    title = fields.CharField(model_attr="title")
    abstract = fields.CharField(model_attr="abstract")
    geography = fields.CharField(model_attr="geography")
    collection = fields.CharField(model_attr="collection", null=True)
    dataset = fields.CharField(model_attr="dataset", null=True)
    publication_year = IntegerField(model_attr="publication_year")
    is_latest = BooleanField(model_attr="is_latest", null=True)
    service_type = fields.CharField(model_attr="service_type", null=True)
    geodata_type = fields.CharField(model_attr="geodata_type", null=True)
    source = fields.CharField(model_attr="source", null=True)
    visibility = fields.CharField(model_attr="visibility")
    crs = fields.CharField(model_attr="crs")
    modified = DateTimeField(model_attr="modified", null=True)
    language = fields.CharField(model_attr="language")
    keywords_en = fields.CharField(model_attr="tags_en", analyzer='english_stemmer')
    keywords_de = fields.CharField(model_attr="tags_de", analyzer='german_stemmer')
    keywords_fr = fields.CharField(model_attr="tags_fr", analyzer='french_stemmer')

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        # autocomplete_string = obj.title
        autocomplete_string = ''
        tags = getattr(obj, 'tags_{}'.format(obj.language))
        if tags is not None:
            autocomplete_string += " ".join(tags)
        return autocomplete_string

    def get_model(self):
        return GeoServiceMetadata

    def index_queryset(self, using=None):
        if using is None or using not in ['de', 'fr', 'en']:
            return self.get_model().objects.filter(language=using)
        # always index all records, more traditional would be to
        # only index the corresponding language using
        # self.get_model().objects.filter(language=using)
        return self.get_model().objects.all()


class EnglishGeoServiceMetadataIndex(GeoServiceMetadataIndex):
    text = fields.CharField(document=True, use_template=True, analyzer='english_stemmer')


class GermanGeoServiceMetadataIndex(GeoServiceMetadataIndex):
    text = fields.CharField(document=True, use_template=True, analyzer='german_stemmer')


class FrenchGeoServiceMetadataIndex(GeoServiceMetadataIndex):
    text = fields.CharField(document=True, use_template=True, analyzer='french_stemmer')
