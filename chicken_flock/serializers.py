# serializers.py

from rest_framework import serializers
from .models import ChickenFlockInfo


class ChickenFlockSerializer(serializers.ModelSerializer):
    batchName = serializers.SerializerMethodField()
    incubationDate = serializers.SerializerMethodField()
    chickenSeedlingNumber = serializers.SerializerMethodField()
    vaccineId = serializers.SerializerMethodField()
    vaccineManufacturers = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = ChickenFlockInfo
        fields = (
            "id", "batchName", "incubationDate", "chickenSeedlingNumber", "vaccineId",
            "vaccineManufacturers", "status")

    def get_batchName(self, obj):
        return obj.batch_name

    def get_incubationDate(self, obj):
        return obj.incubation_date

    def get_chickenSeedlingNumber(self, obj):
        return obj.chicken_seedling_number

    def get_vaccineId(self, obj):
        return obj.vaccine_id

    def get_vaccineManufacturers(self, obj):
        return obj.vaccine_manufacturers

    def get_status(self, obj):
        if obj.status == "0":
            return "已关闭"
        else:
            return "活动中"


class ChickenFlockToSerializer(serializers.ModelSerializer):
    batchName = serializers.SerializerMethodField()
    incubationDate = serializers.SerializerMethodField()
    chickenSeedlingNumber = serializers.SerializerMethodField()
    vaccineId = serializers.SerializerMethodField()
    vaccineManufacturers = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    farmName = serializers.SerializerMethodField()
    farmId = serializers.SerializerMethodField()

    class Meta:
        model = ChickenFlockInfo
        fields = (
            "id", "farmId", "farmName", "batchName", "incubationDate", "chickenSeedlingNumber", "vaccineId",
            "vaccineManufacturers", "status",
            "d1", "d2", "d3")

    def get_batchName(self, obj):
        return obj.batch_name

    def get_incubationDate(self, obj):
        return obj.incubation_date

    def get_chickenSeedlingNumber(self, obj):
        return obj.chicken_seedling_number

    def get_vaccineId(self, obj):
        return obj.vaccine_id

    def get_vaccineManufacturers(self, obj):
        return obj.vaccine_manufacturers

    def get_farmName(self, obj):
        return obj.farm_name

    def get_farmId(self, obj):
        return obj.user_id

    def get_status(self, obj):
        if obj.status == "0":
            return "已关闭"
        else:
            return "活动中"
