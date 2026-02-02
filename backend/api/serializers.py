from rest_framework import serializers
from .models import DataSet

class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ['id', 'name', 'uploaded_at', 'summary']
        read_only_fields = ['id', 'uploaded_at', 'summary']
