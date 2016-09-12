import re
import logging
import shlex

from django.contrib.postgres.search import SearchQuery
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

from api.helpers.networking import is_internal
from api.models import AllRecords, Record, Base
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
            return AllRecords.objects.all()
        return AllRecords.objects.exclude(visibility='hsr-internal')


class RecordDetail(generics.RetrieveAPIView):
    """
    Returns single metadata record.

    Returns 403 error if metadata record is HSR internal and client does not connect from HSR Address or is not authenticated.
    """
    queryset = Record.objects.all()
    serializer_class = AllRecordsSerializer

    def retrieve(self, request, pk=None):
        try:
            record = AllRecords.objects.get(api_id=pk)
            if not self.request.user.is_authenticated and not is_internal(self.request.META['REMOTE_ADDR']):
                if record.visibility == 'hsr-internal':
                    return Response(status=status.HTTP_403_FORBIDDEN)
        except AllRecords.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AllRecordsSerializer(record)
        return Response(serializer.data)


class Search(generics.ListAPIView):
    """
    Fulltext search.

    Search text is passed in query parameter. The search can be controlled with operators, which can be combined:
        - If there is no operator between search words, metadata records matching either word will be returned
        - & for and op. Metadata records matching bot keywords will be returned. E.g. "Zürich & Digital"
        - ! for not op. Records not matching the word will be returned. E.g. "Digital & !Orthofoto"
    """
    serializer_class = AllRecordsSerializer

    @staticmethod
    def search_to_query_string(search_string):
        """
        Parses the passed search_string into a Postgres to_tsquery() compatible string

        Wrong User inputs won't be caught here but when the query is executed
        """
        AND_TOKEN = '&'
        OR_TOKEN = '|'
        NOT_TOKEN = '!'

        search_string = search_string.replace(AND_TOKEN, ' {} '.format(AND_TOKEN))  # ensure whitespace around `&`
        search_string = search_string.replace(AND_TOKEN, ' {} '.format(AND_TOKEN))  # ensure whitespace around `&`
        search_string = search_string.replace(OR_TOKEN, ' {} '.format(OR_TOKEN))  # remove pipes, they are the same as white space
        search_string = search_string.replace(NOT_TOKEN, ' {} '.format(NOT_TOKEN))  # add whitespace around `!`

        lexer = shlex.shlex(search_string)
        operation = None
        for token in lexer:
            if token in [AND_TOKEN, OR_TOKEN, NOT_TOKEN]:
                operation = AND_TOKEN
                continue
            if not operation:
                operation = OR_TOKEN
            if operation == AND_TOKEN:
                sq = sq & SearchQuery(token)


        return ''.join(parsed_string)

        parsed_string = " ".join(search_string.split())
        parsed_string = parsed_string.split('|')
        parsed_string.split('&')
        # Remove all whitespaces around "&" characters
        parsed_string = re.sub(r'\s?([&])\s?', r'\1', parsed_string)
        # Replace all whitespaces with pipes
        condensed = re.sub(r"\s+", '|', parsed_string)
        condensed = condensed.split('&')
        return

    def create_query(self, search_string, internal):
        """
        Parses the passed search_string into a Postgres to_tsquery() compatible string
        """
        language = self.request.query_params.get('language', 'en')
        vector_to_search, pg_language = AllRecords.LANGUAGE_TO_PG.get(language, 'en')

        query = AllRecords.objects
        if not internal:
            query = query.exclude(visibility='hsr-internal')
        filter_kwargs = {
            vector_to_search: search_string
        }
        query = query.filter(**filter_kwargs)
        # query = query.raw(
        #     "SELECT *, ts_rank_cd( " + vector_to_search + """, query) AS rank
        #       FROM all_records, to_tsquery(%s, %s) query
        #       WHERE query @@ """ + vector_to_search + """
        #       ORDER BY rank DESC;""", [pg_language, search_string]
        # )
        return query

    def get_queryset(self):
        search_string = self.request.query_params.get('query', None)

        if search_string:
            internal = self.request.user.is_authenticated or is_internal(self.request.META['REMOTE_ADDR'])
            parsed_search = self.search_to_query_string(search_string)
            try:
                query = list(self.create_query(parsed_search, internal))
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
            return AllRecords.objects.order_by('-modified')[:limit]
        else:
            return AllRecords.objects.exclude(visibility='hsr-internal').order_by('-modified')[:limit]


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
