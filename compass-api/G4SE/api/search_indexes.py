from haystack import indexes

from configurable_elastic_search_backend import fields

from api.models import CombinedRecord


class CombinedRecordIndex(indexes.SearchIndex, indexes.Indexable):

    text = fields.CharField(document=True, use_template=True, analyzer='german_stemmer')
    api_id = fields.CharField(model_attr="api_id", boost=0.1, analyzer='german_stemmer')
    content = fields.CharField(model_attr="content", analyzer='german_stemmer')
    abstract = fields.CharField(model_attr="abstract", analyzer='german_stemmer')
    geography = fields.CharField(model_attr="geography", boost=1.4, analyzer='german_stemmer')
    collection = fields.CharField(model_attr="collection", null=True, analyzer='german_stemmer')
    dataset = fields.CharField(model_attr="dataset", null=True, analyzer='german_stemmer')
    visibility = fields.CharField(model_attr="visibility")
    language = fields.CharField(model_attr="language")

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        autocomplete_string = " ".join((
            obj.content, obj.abstract, obj.geography
        ))
        if obj.collection is not None:
            autocomplete_string += " ".join((obj.collection,))
        if obj.dataset is not None:
            autocomplete_string += " ".join((obj.dataset,))
        if obj.dataset is not None:
            autocomplete_string += " ".join((obj.visibility,))
        return autocomplete_string

    def get_model(self):
        return CombinedRecord

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(language=using)
