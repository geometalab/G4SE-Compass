import re
import logging
from django.db import ProgrammingError
from django.contrib.auth.models import User
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
from api.serializers import AllRecordsSerializer, RecordSerializer, UserSerializer, EditRecordSerializer


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

    def retrieve(self, request, pk=None):
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

    @staticmethod
    def parse_language(language):
        if language == 'de':
            return ['search_vector_de', 'german']
        elif language == 'en':
            return ['search_vector_en', 'english']
        elif language == 'fr':
            return ['search_vector_fr', 'french']
        else:
            raise ParseError('Not a valid language.')

    @staticmethod
    def parse_query(search_string):
        """
        Parses the passed search_string into a Postgres to_tsquery() compatible string

        Wrong User inputs won't be caught here but when the query is executed
        """
        parsed_string = " ".join(search_string.split())
        # Remove all whitespaces around "&" characters
        parsed_string = re.sub(r'\s?([&])\s?', r'\1', parsed_string)
        # Replace all whitespaces with pipes
        return re.sub(r"\s+", '|', parsed_string)

    @staticmethod
    def create_query(search_string, language, internal):
        """
        Parses the passed search_string into a Postgres to_tsquery() compatible string
        """
        exclude = ''
        if not internal:
            exclude = "visibility != 'hsr-internal' AND"

        query = CombinedRecord.objects.raw(
            "SELECT *, ts_rank_cd( " + language[0] + """, query) AS rank
              FROM all_records, to_tsquery(%s, %s) query
              WHERE """ + exclude + """ query @@ """ + language[0] + """
              ORDER BY rank DESC;""", [language[1], search_string]
        )
        return query

    def get_queryset(self):
        search_string = self.request.query_params.get('query', None)
        passed_language = self.request.query_params.get('language', 'de')
        if search_string:
            internal = self.request.user.is_authenticated or is_internal(self.request.META['REMOTE_ADDR'])
            language = self.parse_language(passed_language)
            parsed_search = self.parse_query(search_string)
            try:
                query = list(self.create_query(parsed_search, language, internal))
            except ProgrammingError:
                logger.exception('Invalid Query')
                raise ParseError('Invalid Query')
            return query
        else:
            raise ParseError('The query parameter is mandatory')


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

    def list(self, request):
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

    def retrieve(self, request, pk=None):
        try:
            record = Record.objects.get(api_id=pk)
        except Record.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RecordSerializer(record)
        return Response(serializer.data)
