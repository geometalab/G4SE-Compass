from .models import Record, HarvestedRecord, AllRecords
from django.contrib.auth.models import User
from rest_framework import serializers
import datetime


class AllRecordsSerializer(serializers.ModelSerializer):
    login_name = serializers.HiddenField(default=None)
    search_vector_de = serializers.HiddenField(default=None)
    search_vector_en = serializers.HiddenField(default=None)
    search_vector_fr = serializers.HiddenField(default=None)

    class Meta:
        model = AllRecords
        fields = '__all__'


class RecordSerializer(serializers.ModelSerializer):
    login_name = serializers.HiddenField(default=None)
    search_vector_de = serializers.HiddenField(default=None)
    search_vector_en = serializers.HiddenField(default=None)
    search_vector_fr = serializers.HiddenField(default=None)

    class Meta:
        model = Record
        fields = '__all__'


class HarvestedRecordSerializer(serializers.ModelSerializer):
    login_name = serializers.HiddenField(default=None)
    search_vector_de = serializers.HiddenField(default=None)
    search_vector_en = serializers.HiddenField(default=None)
    search_vector_fr = serializers.HiddenField(default=None)

    class Meta:
        model = HarvestedRecord
        fields = '__all__'


class EditRecordSerializer(serializers.ModelSerializer):
    modified = serializers.HiddenField(default=datetime.datetime.now())
    search_vector_de = serializers.HiddenField(default=None)
    search_vector_en = serializers.HiddenField(default=None)
    search_vector_fr = serializers.HiddenField(default=None)

    def validate_login_name(self, value):
        user = self.context['request'].user.username
        if not value:
            return user
        return value

    class Meta:
        model = Record
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
