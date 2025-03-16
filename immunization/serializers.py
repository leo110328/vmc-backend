# serializers.py

from rest_framework import serializers
from .models import ImmunizationInfo


class ImmunizationInfoSerializer(serializers.ModelSerializer):
    periodValidity = serializers.SerializerMethodField()
    vaccineName = serializers.SerializerMethodField()
    vaccineType = serializers.SerializerMethodField()
    vaccineBatch = serializers.SerializerMethodField()
    vaccineDate = serializers.SerializerMethodField()
    vaccineFrequency = serializers.SerializerMethodField()
    vaccineDosage = serializers.SerializerMethodField()
    vaccineRoute = serializers.SerializerMethodField()
    vaccineManufacturers = serializers.SerializerMethodField()
    vaccineAddress = serializers.SerializerMethodField()
    dataTime = serializers.SerializerMethodField()

    class Meta:
        model = ImmunizationInfo
        fields = (
            "id", "periodValidity", "vaccineName", "vaccineType", "vaccineBatch", "vaccineDate", "vaccineFrequency",
            "vaccineDosage", "vaccineRoute", "vaccineManufacturers", "vaccineAddress", "dataTime")

    def get_periodValidity(self, obj):
        return obj.period_validity

    def get_vaccineName(self, obj):
        return obj.vaccine_name

    def get_vaccineType(self, obj):
        return obj.vaccine_type

    def get_vaccineBatch(self, obj):
        return obj.vaccine_batch

    def get_vaccineDate(self, obj):
        return obj.vaccine_date

    def get_vaccineFrequency(self, obj):
        return obj.vaccine_frequency

    def get_vaccineDosage(self, obj):
        return obj.vaccine_dosage

    def get_vaccineRoute(self, obj):
        return obj.vaccine_route

    def get_vaccineManufacturers(self, obj):
        return obj.vaccine_manufacturers

    def get_vaccineAddress(self, obj):
        return obj.vaccine_address

    def get_dataTime(self, obj):
        return obj.data_time
