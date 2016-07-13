from api.models import Record, HarvestedRecord, AllRecords
from api.serializers import RecordSerializer, AllRecordsSerializer
from rest_framework import generics


class RecordList(generics.ListAPIView):
    queryset = AllRecords.objects.all()
    serializer_class = AllRecordsSerializer


class RecordDetail(generics.RetrieveAPIView):
    queryset = AllRecords.objects.all()
    serializer_class = AllRecordsSerializer
