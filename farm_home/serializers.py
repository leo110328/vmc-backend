# serializers.py

from rest_framework import serializers
from .models import FarmHomeInfo


class FarmHomeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmHomeInfo
        fields = "__all__"
