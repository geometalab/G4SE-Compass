import datetime

from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers
from rest_framework.utils.field_mapping import get_field_kwargs

from api.search_indexes import GeoServiceMetadataIndex
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
    @staticmethod
    def _get_default_field_kwargs(model, field):
        """
        Get the required attributes from the model field in order
        to instantiate a REST Framework serializer field.
        """
        if not hasattr(model._meta, '_get_all_field_names'):
            kwargs = {}
            try:
                model_field = model._meta.get_field(field.model_attr)
            except:
                return kwargs
            kwargs = get_field_kwargs(field.model_attr, model_field)

            # Remove stuff we don't care about!
            delete_attrs = [
                "allow_blank",
                "choices",
                "model_field",
            ]
            for attr in delete_attrs:
                if attr in kwargs:
                    del kwargs[attr]
            return kwargs
        else:
            return HaystackSerializer._get_default_field_kwargs(model, field)

    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [GeoServiceMetadataIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = [
            "text", "title", "abstract", "geography", "collection", "dataset",
            "autocomplete", "api_id", "visibility", "publication_year",
            "service_type", "source", "highlighted",
            "keywords_en", "keywords_de", "keywords_fr",
        ]

