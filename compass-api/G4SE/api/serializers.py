from .models import Record, HarvestedRecord, AllRecords
from django.contrib.auth.models import User
from rest_framework import serializers
import datetime


class AllRecordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AllRecords


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Record


class EditRecordSerializer(serializers.ModelSerializer):
    modified = serializers.HiddenField(default=datetime.datetime.now())

    def validate_login_name(self, value):
        user = self.context['request'].user.username
        if not value:
            return user
        return value

    class Meta:
        model = Record


class HarvestedRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = HarvestedRecord


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
