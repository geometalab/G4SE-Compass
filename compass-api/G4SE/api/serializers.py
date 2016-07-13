from .models import Record, HarvestedRecord, AllRecords
from rest_framework import serializers


class AllRecordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AllRecords


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Record


class HarvestedRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = HarvestedRecord
