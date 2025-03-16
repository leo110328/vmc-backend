# serializers.py

from rest_framework import serializers
from .models import MedicationUseInfo


class MedicationUseInfoSerializer(serializers.ModelSerializer):
    chickenId = serializers.SerializerMethodField()
    chickenName = serializers.SerializerMethodField()
    medicationName = serializers.SerializerMethodField()
    medicationDose = serializers.SerializerMethodField()
    medicationMeasure = serializers.SerializerMethodField()
    usageDuration = serializers.SerializerMethodField()
    dataTime = serializers.SerializerMethodField()

    class Meta:
        model = MedicationUseInfo
        fields = (
            "id", "chickenId", "chickenName", "medicationName", "medicationDose", "medicationMeasure", "usageDuration",
            "dataTime")

    def get_chickenId(self, obj):
        return obj.chicken_flock_id

    def get_chickenName(self, obj):
        return obj.chicken_name

    def get_medicationName(self, obj):
        return obj.medication_name

    def get_medicationDose(self, obj):
        return obj.medication_dose

    def get_medicationMeasure(self, obj):
        return obj.medication_measure

    def get_usageDuration(self, obj):
        return obj.usage_duration

    def get_dataTime(self, obj):
        return obj.data_time
