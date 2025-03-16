# serializers.py

from rest_framework import serializers
from .models import FarmOtherAttributesInfo


class FarmOtherAttributesSerializer(serializers.ModelSerializer):
    dataTime = serializers.SerializerMethodField()
    farmId = serializers.SerializerMethodField()
    bacterialType = serializers.SerializerMethodField()

    class Meta:
        model = FarmOtherAttributesInfo
        fields = ("id", "farmId", "dataTime", "sensitive", "intermediate", "resistant", "antibiotic", "bacterialType")

    def get_farmId(self, obj):
        return obj.farm_id

    def get_dataTime(self, obj):
        return obj.data_time

    def get_bacterialType(self, obj):
        return obj.bacterial_type
