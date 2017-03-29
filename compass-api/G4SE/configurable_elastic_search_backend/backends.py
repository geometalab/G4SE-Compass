from haystack.backends.elasticsearch_backend import ElasticsearchSearchBackend, ElasticsearchSearchEngine


class ConfigurableElasticBackend(ElasticsearchSearchBackend):
    DEFAULT_ANALYZER = "snowball"

    # removed all allowed characters which a user should be allowed to define
    RESERVED_CHARACTERS = [
        char for char in ElasticsearchSearchBackend.RESERVED_CHARACTERS
        if char not in [
            '"', '~', '*', '?', '(', ')', '^',
        ]
    ]

    def __init__(self, connection_alias, **connection_options):
        super().__init__(connection_alias, **connection_options)

        options = connection_options.get("OPTIONS", {})

        self.DEFAULT_SETTINGS = options.get('settings', self.DEFAULT_SETTINGS)
        self.DEFAULT_ANALYZER = options.get('DEFAULT_ANALYZER', self.DEFAULT_ANALYZER)

    def build_schema(self, fields):
        content_field_name, mapping = super().build_schema(fields)
        for field_name, field_class in fields.items():
            field_mapping = mapping[field_class.index_fieldname]
            if field_mapping['type'] == 'string' and field_class.indexed:
                if not hasattr(field_class, 'facet_for') and field_class.field_type not in ('ngram', 'edge_ngram'):
                    field_mapping['analyzer'] = self.DEFAULT_ANALYZER
                    if hasattr(field_class, 'analyzer') and field_class.analyzer is not None:
                        field_mapping['analyzer'] = field_class.analyzer
            mapping.update({field_class.index_fieldname: field_mapping})
        return (content_field_name, mapping)


class EnglishStemmerElasticBackend(ConfigurableElasticBackend):
    DEFAULT_ANALYZER = "english_stemmer"


class GermanStemmerElasticBackend(ConfigurableElasticBackend):
    DEFAULT_ANALYZER = "german_stemmer"


class FrenchStemmerElasticBackend(ConfigurableElasticBackend):
    DEFAULT_ANALYZER = "french_stemmer"


class ConfigurableElasticEngine(ElasticsearchSearchEngine):
    backend = ConfigurableElasticBackend


class EnglishConfigurableElasticEngine(ElasticsearchSearchEngine):
    backend = EnglishStemmerElasticBackend


class GermanConfigurableElasticEngine(ElasticsearchSearchEngine):
    backend = EnglishStemmerElasticBackend


class FrenchConfigurableElasticEngine(ElasticsearchSearchEngine):
    backend = FrenchStemmerElasticBackend
