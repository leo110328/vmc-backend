# serializers.py

from rest_framework import serializers
from .models import ClearProcedureInfo


class ClearProcedureInfoSerializer(serializers.ModelSerializer):
    parasitesInternal = serializers.SerializerMethodField()
    parasitesExternal = serializers.SerializerMethodField()
    periodValidity = serializers.SerializerMethodField()
    dataTime = serializers.SerializerMethodField()

    class Meta:
        model = ClearProcedureInfo
        fields = (
            "id", "periodValidity", "detergent", "dentifrices", "pesticide", "parasitesInternal", "parasitesExternal",
            "dataTime")

    def get_periodValidity(self, obj):
        return obj.period_validity

    def get_parasitesInternal(self, obj):
        return obj.parasites_internal

    def get_parasitesExternal(self, obj):
        return obj.parasites_external

    def get_dataTime(self, obj):
        return obj.data_time
