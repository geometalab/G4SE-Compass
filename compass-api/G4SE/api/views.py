import logging

import grako
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from grako.exceptions import FailedParse
from rest_framework import filters
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework.settings import api_settings
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from api.filters import RecordSearch, LimitRecordFilter
from api.helpers.helpers import is_internal
from api.models import CombinedRecord, Record
from api.serializers import AllRecordsSerializer, UserSerializer, EditRecordSerializer

logger = logging.getLogger(__name__)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Fix for CSRF error on put and delete requests after upgrade from 3.3 to 3.4, overwirte csrf check to do nothing
    """
    def enforce_csrf(self, request):
        return


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
