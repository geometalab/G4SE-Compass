from api.models import AllRecords, Record
from api.serializers import AllRecordsSerializer, RecordSerializer, UserSerializer, EditRecordSerializer
from django.contrib.auth.models import User
from rest_framework import generics, filters, permissions
from rest_framework.response import Response
from django.contrib.postgres.search import SearchVector
from rest_framework import status


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

    def list(self, request):
        queryset = self.get_queryset()
        serializer = RecordSerializer(queryset, many=True)
        return Response(serializer.data)


class CreateRecord(generics.CreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


class CreateAndEditRecord(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def retrieve(self, request, pk=None):
        try:
            record = Record.objects.get(api_id=pk)
        except Record.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RecordSerializer(record)
        return Response(serializer.data)
