from .models import Record, CombinedRecord
from django.contrib.auth.models import User
from rest_framework import serializers
import datetime


class BaseRecordSerializer(serializers.ModelSerializer):
    login_name = serializers.HiddenField(default=None)
    search_vector_de = serializers.HiddenField(default=None)
    search_vector_en = serializers.HiddenField(default=None)
    search_vector_fr = serializers.HiddenField(default=None)


class AllRecordsSerializer(BaseRecordSerializer):
    content = serializers.CharField(max_length=200)

    class Meta:
        model = CombinedRecord
        fields = '__all__'


class RecordSerializer(BaseRecordSerializer):
    class Meta:
        model = Record
        fields = '__all__'


class EditRecordSerializer(BaseRecordSerializer):
    modified = serializers.HiddenField(default=datetime.datetime.now())

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
