import logging

import grako
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from drf_haystack.filters import HaystackHighlightFilter, HaystackFilter
from drf_haystack.viewsets import HaystackViewSet
from grako.exceptions import FailedParse
from haystack.inputs import Raw, Clean
from haystack.query import SearchQuerySet
from rest_framework import filters
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework.settings import api_settings
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from api.filters import RecordSearch, LimitRecordFilter, DateLimitRecordFilter, DateLimitSearchRecordFilter
from api.helpers.helpers import is_internal
from api.models import CombinedRecord, Record
from api.search_indexes import CombinedRecordIndex, EnglishCombinedRecordIndex, GermanCombinedRecordIndex, \
    FrenchCombinedRecordIndex
from api.serializers import AllRecordsSerializer, UserSerializer, EditRecordSerializer, CombinedRecordsSearchSerializer

logger = logging.getLogger(__name__)


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='G4SE API')
    return response.Response(generator.get_schema(request=request))


class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class MetaDataReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Returns all metadata records visible to the client.
    """
    serializer_class = AllRecordsSerializer
    pagination_class = StandardResultsSetPagination
    queryset = CombinedRecord.objects.all()
    ordering_parameter = api_settings.ORDERING_PARAM
    ordering = '-modified'

    filter_backends = (
        filters.OrderingFilter,
        RecordSearch,
        LimitRecordFilter,
        DateLimitRecordFilter,
    )

    def get_queryset(self):
        query = super().get_queryset()
        internal = self.request.user.is_authenticated or is_internal(self.request.META['REMOTE_ADDR'])
        if not self.request.query_params.get(self.ordering_parameter, False):
            query.order_by(self.ordering)
        # TODO: make this into an optional list of publicity
        if not internal:
            query = query.filter(visibility=CombinedRecord.PUBLIC)
        return query

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            record = CombinedRecord.objects.get(api_id=pk)
            if not self.request.user.is_authenticated and not is_internal(self.request.META['REMOTE_ADDR']):
                if record.visibility == 'hsr-internal':
                    return Response(status=status.HTTP_403_FORBIDDEN)
        except CombinedRecord.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AllRecordsSerializer(record)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except grako.exceptions.FailedParse as e:
            error_message = e.message
            logger.error(error_message)
            user_message = _("Couldn't process the query. Ensure the syntax is correct and try again.")
            return Response({'error_message': user_message, 'error_detail': error_message},
                            status=status.HTTP_400_BAD_REQUEST)


class RecordsAdminViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Record.objects.all()
    serializer_class = EditRecordSerializer
    pagination_class = SmallResultsSetPagination


class CombinedRecordsSearchView(HaystackViewSet):
    # `index_models` is an optional list of which models you would like to include
    # in the search result. You might have several models indexed, and this provides
    # a way to filter out those of no interest for this particular view.
    # (Translates to `SearchQuerySet().models(*index_models)` behind the scenes.
    FALLBACK_LANGUAGE = CombinedRecord.ENGLISH
    pagination_class = StandardResultsSetPagination
    index_models = [
        CombinedRecordIndex,
        EnglishCombinedRecordIndex,
        GermanCombinedRecordIndex,
        FrenchCombinedRecordIndex,
    ]
    document_uid_field = "api_id"
    filter_backends = [
        HaystackFilter,
        HaystackHighlightFilter,
        DateLimitSearchRecordFilter,
    ]
    serializer_class = CombinedRecordsSearchSerializer

    def get_queryset(self):
        using = self.request.GET.get('language', self.FALLBACK_LANGUAGE)
        queryset = SearchQuerySet().using(using)
        query_string = self.request.GET.get('q', None)
        if query_string is None or query_string == '':
            return queryset
        cleaned_query_string = Clean(query_string)
        sqs_raw = queryset.filter(text=Raw(cleaned_query_string.query_string))
        internal = self.request.user.is_authenticated or is_internal(self.request.META['REMOTE_ADDR'])
        # TODO: make this into an optional list of publicity
        if not internal:
            sqs_raw = sqs_raw.filter(visibility=CombinedRecord.PUBLIC)
        return sqs_raw
