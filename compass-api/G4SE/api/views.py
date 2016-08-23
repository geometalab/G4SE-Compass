from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from api.helpers.helpers import is_internal
from api.models import AllRecords, Record
from api.serializers import AllRecordsSerializer, RecordSerializer, UserSerializer, EditRecordSerializer


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
    tbd.
    """
    serializer_class = AllRecordsSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        if query:
            if self.request.user.is_authenticated or is_internal(self.request.META['REMOTE_ADDR']):
                return AllRecords.objects.annotate(
                    search=SearchVector('content', 'abstract', 'geography', 'collection', 'dataset'),
                ).filter(search=query)
            else:
                return AllRecords.objects.annotate(
                    search=SearchVector('content', 'abstract', 'geography', 'collection', 'dataset'),
                ).filter(search=query).exclude(visibility='hsr-internal')
        return AllRecords.objects.all()


class MostRecentRecords(generics.ListAPIView):
    """
    Returns the most recently entered or modified records
    Count may be passed, default is 5
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
    queryset = Record.objects.all()
    serializer_class = EditRecordSerializer

    def retrieve(self, request, pk=None):
        try:
            record = Record.objects.get(api_id=pk)
        except Record.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RecordSerializer(record)
        return Response(serializer.data)
