from .models import Record, HarvestedRecord, AllRecords
from django.contrib.auth.models import User
from rest_framework import serializers
import datetime


class AllRecordsSerializer(serializers.ModelSerializer):
    login_name = serializers.HiddenField(default=None)

    class Meta:
        model = AllRecords


class RecordSerializer(serializers.ModelSerializer):
    login_name = serializers.HiddenField(default=None)

    class Meta:
        model = Record


class HarvestedRecordSerializer(serializers.ModelSerializer):
    login_name = serializers.HiddenField(default=None)

    class Meta:
        model = HarvestedRecord


class EditRecordSerializer(serializers.ModelSerializer):
    modified = serializers.HiddenField(default=datetime.datetime.now())

    def validate_login_name(self, value):
        user = self.context['request'].user.username
        if not value:
            return user
        return value

    class Meta:
        model = Record


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
