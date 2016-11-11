import datetime

from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers

from api.search_indexes import GeoServiceMetadataIndex, EnglishGeoServiceMetadataIndex, GermanGeoServiceMetadataIndex, \
    FrenchGeoServiceMetadataIndex
from .models import GeoServiceMetadata, GEO_SERVICE_METADATA_AGREED_FIELDS


class GeoServiceMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoServiceMetadata
        fields = GEO_SERVICE_METADATA_AGREED_FIELDS


class EditRecordSerializer(serializers.ModelSerializer):
    api_id = serializers.HyperlinkedIdentityField(
        view_name='admin-detail',
        lookup_field='api_id',
        lookup_url_kwarg='pk'
    )
    modified = serializers.ReadOnlyField(default=datetime.datetime.now())

    def validate(self, attrs):
        validated_values = super().validate(attrs=attrs)
        for key, value in validated_values.items():
            if value == '':
                validated_values[key] = None
        return validated_values

    def validate_extent(self, value):
        if value == '':
            return None
        return value

    def validate_login_name(self, value):
        user = self.context['request'].user.username
        if not value:
            return user
        return value

    class Meta:
        model = GeoServiceMetadata
        fields = GEO_SERVICE_METADATA_AGREED_FIELDS


def get_all_field_names(model):
    from itertools import chain
    return list(set(chain.from_iterable(
        (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
        for field in model._meta.get_fields()
        # For complete backwards compatibility, you may want to exclude
        # GenericForeignKey from the results.
        if not (field.many_to_one and field.related_model is None)
    )))


class GeoServiceMetadataSearchSerializer(HaystackSerializer):
    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [
            GeoServiceMetadataIndex,
            EnglishGeoServiceMetadataIndex,
            GermanGeoServiceMetadataIndex,
            FrenchGeoServiceMetadataIndex,
        ]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = [
            "text", "title", "abstract", "geography", "collection", "dataset",
            "autocomplete", "api_id", "visibility", "publication_year",
            "service_type", "source", "highlighted",
            "keywords_en", "keywords_de", "keywords_fr",
        ]
