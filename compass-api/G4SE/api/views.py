import logging
from collections import OrderedDict

import django_filters
from drf_haystack.filters import HaystackHighlightFilter
from drf_haystack.viewsets import HaystackViewSet
from haystack.query import SearchQuerySet
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, renderer_classes, list_route
from rest_framework import response, schemas
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from api.filters import LimitRecordFilter, DateLimitRecordFilter, DateLimitSearchRecordFilter, \
    IsLatestSearchRecordFilter, MetadataSearchFilter, MetadataSearchOrderingFilter
from api.helpers.helpers import is_internal
from api.helpers.input import ElasticSearchExtendedAutoQuery
from api.models import GeoServiceMetadata
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
        django_filters.rest_framework.DjangoFilterBackend,
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
        GeoServiceMetadata,
    ]
    document_uid_field = "api_id"
    filter_backends = [
        HaystackHighlightFilter,
        DateLimitSearchRecordFilter,
        IsLatestSearchRecordFilter,
        django_filters.rest_framework.DjangoFilterBackend,
        MetadataSearchFilter,
        MetadataSearchOrderingFilter,
    ]
    serializer_class = GeoServiceMetadataSearchSerializer

    def get_queryset(self, index_models=[]):
        using = self.request.GET.get('language', self.FALLBACK_LANGUAGE)
        qs = super().get_queryset(index_models).using(using)

        internal = self.request.user.is_authenticated or is_internal(self.request.META['REMOTE_ADDR'])
        # TODO: make this into an optional list of publicity
        if not internal:
            qs = qs.filter(visibility=GeoServiceMetadata.VISIBILITY_PUBLIC)
        return qs

    @list_route()
    def actual(self, request):
        query_string = request.GET.get('search', '')
        if query_string != '':
            using = request.GET.get('language', self.FALLBACK_LANGUAGE)
            cleaned_query_string = ElasticSearchExtendedAutoQuery(query_string)
            searched_for = cleaned_query_string.prepare(SearchQuerySet().using(using).query)
        else:
            searched_for = ''
        return Response(OrderedDict([
            ('search', query_string),
            ('actual_search', searched_for),
        ]))
