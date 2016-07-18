from api.models import AllRecords, Record
from api.serializers import AllRecordsSerializer, RecordSerializer
from rest_framework import generics, filters
from django.contrib.postgres.search import SearchVector


class AllRecordsList(generics.ListAPIView):
    """
    View to return all records in the database
    """
    queryset = AllRecords.objects.all()
    serializer_class = AllRecordsSerializer


class RecordDetail(generics.RetrieveAPIView):
    """
    Detail view for single record
    """
    queryset = AllRecords.objects.all()
    serializer_class = AllRecordsSerializer


class Search(generics.ListAPIView):
    """
    Main search view
    """
    serializer_class = AllRecordsSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        if query:
            return AllRecords.objects.annotate(
                search=SearchVector('content', 'abstract', 'geography', 'collection', 'dataset'),
            ).filter(search=query)
        return AllRecords.objects.all()


class InternalRecordsList(generics.ListCreateAPIView):
    """
    List/Create view for internal records only
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


class EditRecord(generics.RetrieveUpdateDestroyAPIView):
    """
    View for editing an internal record
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
