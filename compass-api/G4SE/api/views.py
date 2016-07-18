from api.models import AllRecords, Record
from api.serializers import AllRecordsSerializer, RecordSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics, filters, permissions
from django.contrib.postgres.search import SearchVector


class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AllRecordsList(generics.ListAPIView):
    queryset = AllRecords.objects.all()
    serializer_class = AllRecordsSerializer


class RecordDetail(generics.RetrieveAPIView):
    queryset = AllRecords.objects.all()
    serializer_class = AllRecordsSerializer


class Search(generics.ListAPIView):
    serializer_class = AllRecordsSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        if query:
            return AllRecords.objects.annotate(
                search=SearchVector('content', 'abstract', 'geography', 'collection', 'dataset'),
            ).filter(search=query)
        return AllRecords.objects.all()


class InternalRecordsList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


class CreateAndEditRecord(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
