# serializers.py

from rest_framework import serializers
from .models import ResourcesInfo


class ResourcesInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourcesInfo
        fields = ("id",)
