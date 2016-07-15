from api.models import Record, AllRecords
from api.serializers import RecordSerializer, AllRecordsSerializer
from rest_framework import generics, filters
from django.contrib.postgres.search import SearchVector


class RecordList(generics.ListAPIView):
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
