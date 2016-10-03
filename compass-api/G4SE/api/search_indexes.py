from haystack import indexes

from configurable_elastic_search_backend import fields

from api.models import CombinedRecord, RecordTag


class CombinedRecordIndex(indexes.BasicSearchIndex, indexes.Indexable):
    STEMMER = 'german_stemmer'
    text = fields.CharField(document=True, use_template=True, analyzer=STEMMER)
    api_id = fields.CharField(model_attr="api_id", boost=0.1, analyzer=STEMMER)
    content = fields.CharField(model_attr="content", analyzer=STEMMER)
    abstract = fields.CharField(model_attr="abstract", analyzer=STEMMER)
    geography = fields.CharField(model_attr="geography", boost=1.4, analyzer=STEMMER)
    collection = fields.CharField(model_attr="collection", null=True, analyzer=STEMMER)
    dataset = fields.CharField(model_attr="dataset", null=True, analyzer=STEMMER)
    visibility = fields.CharField(model_attr="visibility")
    language = fields.CharField(model_attr="language")
    keywords_en = fields.CharField(model_attr="tags_en")
    keywords_de = fields.CharField(model_attr="tags_de")
    keywords_fr = fields.CharField(model_attr="tags_fr")

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
        if obj.tags_en is not None:
            autocomplete_string += " ".join(obj.tags_en)
        if obj.tags_de is not None:
            autocomplete_string += " ".join(obj.tags_de)
        if obj.tags_fr is not None:
            autocomplete_string += " ".join(obj.tags_fr)
        return autocomplete_string

    def get_model(self):
        return CombinedRecord

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(language=using)


class EnglishCombinedRecordIndex(CombinedRecordIndex):
    STEMMER = 'english_stemmer'


class GermanCombinedRecordIndex(CombinedRecordIndex):
    STEMMER = 'german_stemmer'


class FrenchCombinedRecordIndex(CombinedRecordIndex):
    STEMMER = 'french_stemmer'


class RecordTagIndex(indexes.BasicSearchIndex, indexes.Indexable):
    STEMMER = 'german_stemmer'
    text = fields.CharField(document=True, use_template=True, analyzer=STEMMER)
    id = fields.CharField(model_attr="id", boost=0.1, analyzer=STEMMER)
    tag = None
    tag_synonyms = None
    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        autocomplete_string = " ".join((
            obj.tag_en, obj.tag_de, obj.tag_fr
        ))
        if obj.tag_alternatives_de is not None:
            autocomplete_string += " ".join(obj.tag_alternatives_de)
        if obj.tag_alternatives_en is not None:
            autocomplete_string += " ".join(obj.tag_alternatives_en)
        if obj.tag_alternatives_fr is not None:
            autocomplete_string += " ".join(obj.tag_alternatives_fr)
        return autocomplete_string

    def get_model(self):
        return RecordTag

    def index_queryset(self, using=None):
        if using in [c[0] for c in CombinedRecord.language_choices]:
            STEMMERS = dict(
                en='english_stemmer',
                de='german_stemmer',
                fr='french_stemmer',
            )
            stemmer = STEMMERS[using]
            self.tag = fields.CharField(model_attr="tag_{}".format(using), analyzer=stemmer)
            self.tag_synonyms = fields.CharField(model_attr="tag_alternatives_{}".format(using), analyzer=stemmer)
            return self.get_model().objects.all()
        # hack to return no object
        return self.get_model().objects.filter(id__isnull=True)
