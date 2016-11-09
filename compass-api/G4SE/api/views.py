import logging

from drf_haystack.filters import HaystackHighlightFilter, HaystackFilter
from drf_haystack.viewsets import HaystackViewSet
from haystack.backends import SQ
from haystack.inputs import Raw, Clean
from haystack.query import SearchQuerySet
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework.settings import api_settings
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from api.filters import LimitRecordFilter, DateLimitRecordFilter, DateLimitSearchRecordFilter, \
    IsLatestSearchRecordFilter
from api.helpers.helpers import is_internal
from api.models import GeoServiceMetadata
from api.search_indexes import GeoServiceMetadataIndex, EnglishGeoServiceMetadataIndex, GermanGeoServiceMetadataIndex, \
    FrenchGeoServiceMetadataIndex
from api.serializers import EditRecordSerializer, GeoServiceMetadataSearchSerializer, \
    GeoServiceMetadataSerializer

logger = logging.getLogger(__name__)


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='G4SE API')
    return response.Response(generator.get_schema(request=request))


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class MetaDataReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Returns all metadata records visible to the client.
    """
    serializer_class = GeoServiceMetadataSerializer
    pagination_class = StandardResultsSetPagination
    queryset = GeoServiceMetadata.objects.all()
    ordering_parameter = api_settings.ORDERING_PARAM
    ordering = '-modified'
    lookup_url_kwarg = 'pk'
    lookup_field = 'api_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        internal = self.request.user.is_authenticated or is_internal(self.request.META['REMOTE_ADDR'])
        # TODO: make this into an optional list of publicity
        if not internal:
            queryset = queryset.filter(visibility=GeoServiceMetadata.VISIBILITY_PUBLIC)
        return queryset

    filter_backends = (
        filters.OrderingFilter,
        LimitRecordFilter,
        DateLimitRecordFilter,
    )


class GeoServiceMetadataAdminViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = GeoServiceMetadata.objects.filter(imported=False)
    serializer_class = EditRecordSerializer
    pagination_class = SmallResultsSetPagination


class GeoServiceMetadataSearchView(HaystackViewSet):
    # `index_models` is an optional list of which models you would like to include
    # in the search result. You might have several models indexed, and this provides
    # a way to filter out those of no interest for this particular view.
    # (Translates to `SearchQuerySet().models(*index_models)` behind the scenes.
    FALLBACK_LANGUAGE = GeoServiceMetadata.ENGLISH
    pagination_class = StandardResultsSetPagination
    index_models = [
        GeoServiceMetadataIndex,
        EnglishGeoServiceMetadataIndex,
        GermanGeoServiceMetadataIndex,
        FrenchGeoServiceMetadataIndex,
    ]
    document_uid_field = "api_id"
    filter_backends = [
        HaystackFilter,
        HaystackHighlightFilter,
        DateLimitSearchRecordFilter,
        IsLatestSearchRecordFilter,
    ]
    serializer_class = GeoServiceMetadataSearchSerializer

    def get_queryset(self):
        using = self.request.GET.get('language', self.FALLBACK_LANGUAGE)
        queryset = SearchQuerySet().using(using)
        internal = self.request.user.is_authenticated or is_internal(self.request.META['REMOTE_ADDR'])
        # TODO: make this into an optional list of publicity
        if not internal:
            queryset = queryset.filter(visibility=GeoServiceMetadata.VISIBILITY_PUBLIC)

        query_string = self.request.GET.get('search', None)
        if query_string is None or query_string == '':
            return queryset
        cleaned_query_string = Raw(Clean(query_string).query_string)
        keyword_search = {'keywords_{}'.format(using): cleaned_query_string}

        sqs_raw = queryset.filter(
            SQ(text=cleaned_query_string) |
            SQ(abstract=cleaned_query_string) |
            SQ(title=cleaned_query_string) |
            SQ(**keyword_search) |
            SQ(geography=cleaned_query_string) |
            SQ(collection=cleaned_query_string) |
            SQ(dataset=cleaned_query_string)
        )
        return sqs_raw
