import logging

import grako
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from grako.exceptions import FailedParse
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from api.helpers.helpers import is_internal
from api.models import CombinedRecord, Record
from api.search_parser import search_query_parser
from api.search_parser.query_parser import SearchSemantics
from api.serializers import AllRecordsSerializer, RecordSerializer, UserSerializer, EditRecordSerializer
from db import VectorFieldSearchRank

logger = logging.getLogger(__name__)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Fix for CSRF error on put and delete requests after upgrade from 3.3 to 3.4, overwirte csrf check to do nothing
    """
    def enforce_csrf(self, request):
        return


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
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


class AllRecordsList(generics.ListAPIView):
    """
    Returns all metadata records visible to the client.
    """
    serializer_class = AllRecordsSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated or is_internal(self.request.META['REMOTE_ADDR']):
            return CombinedRecord.objects.all()
        return CombinedRecord.objects.exclude(visibility='hsr-internal')


class RecordDetail(generics.RetrieveAPIView):
    """
    Returns single metadata record.

    Returns 403 error if metadata record is HSR internal and client does not connect from HSR Address or is not authenticated.
    """
    queryset = Record.objects.all()
    serializer_class = AllRecordsSerializer

    def retrieve(self, request,  *args, **kwargs):
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


class Search(generics.ListAPIView):
    """
    Fulltext search.

    Search text is passed in query parameter. The search can be controlled with operators, which can be combined:
        - If there is no operator between search words, metadata records matching either word will be returned
        - & for and operation. Metadata records matching bot keywords will be returned. E.g. "Zürich & Digital"
        - ! for not operation. Records not matching the word will be returned. E.g. "Digital & !Orthofoto"
    """
    serializer_class = AllRecordsSerializer

    LANGUAGE_CONFIG_MATCH = dict(
        de='german',
        en='english',
        fr='french',
    )

    def config_for_language(self, language):
        return self.LANGUAGE_CONFIG_MATCH[language]

    def create_query(self, search_string, language, internal):
        """
        Parses the passed search_string into a Postgres to_tsquery() compatible string
        """

        query = CombinedRecord.objects

        if not internal:
            query = query.filter(visibility=CombinedRecord.PUBLIC)

        search_query = search_query_parser.UnknownParser().parse(
            search_string,
            semantics=SearchSemantics(config=self.config_for_language(language))
        )
        vector = 'search_vector_{}'.format(language)
        rank = VectorFieldSearchRank(vector, search_query)
        return query.filter(search_vector_de=search_query).annotate(rank=rank).order_by('-rank')

    def get_queryset(self):
        search_string = self.request.query_params.get('query', None)
        passed_language = self.request.query_params.get('language', 'de')
        if search_string:
            internal = self.request.user.is_authenticated or is_internal(self.request.META['REMOTE_ADDR'])
            return self.create_query(search_string, passed_language, internal)
        else:
            raise ParseError('The query parameter is mandatory')

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except grako.exceptions.FailedParse as e:
            error_message = e.message
            logger.error(error_message)
            user_message = _("Couldn't process the query. Ensure the syntax is correct and try again.")
            return Response({'error_message': user_message, 'error_detail': error_message}, status=status.HTTP_400_BAD_REQUEST)



class MostRecentRecords(generics.ListAPIView):
    """
    Recently entered or modified records

    Return list of recently entered records sorted by date. Count may be passed, default is 5
    """
    serializer_class = AllRecordsSerializer

    def get_queryset(self):
        count = self.request.query_params.get('count', 5)
        try:
            limit = int(count)
        except ValueError:
            raise ParseError('Count must be an Integer.')

        if self.request.user.is_authenticated or is_internal(self.request.META['REMOTE_ADDR']):
            return CombinedRecord.objects.order_by('-modified')[:limit]
        else:
            return CombinedRecord.objects.exclude(visibility='hsr-internal').order_by('-modified')[:limit]


class InternalRecordsList(generics.ListCreateAPIView):
    """
    Show all HSR metadata Records.

    User must be an authenticated administrator access this API view.
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Record.objects.all()
    serializer_class = EditRecordSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = RecordSerializer(queryset, many=True)
        return Response(serializer.data)


class CreateRecord(generics.CreateAPIView):
    """
    Insert a new metadata record.
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Record.objects.all()
    serializer_class = EditRecordSerializer


class CreateAndEditRecord(generics.RetrieveUpdateDestroyAPIView):
    """
    Edit a metadata record.
    """
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Record.objects.all()
    serializer_class = EditRecordSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            record = Record.objects.get(api_id=pk)
        except Record.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RecordSerializer(record)
        return Response(serializer.data)
