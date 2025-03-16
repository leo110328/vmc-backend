# serializers.py

from rest_framework import serializers
from .models import ObituaryInfo


class ObituaryInfoSerializer(serializers.ModelSerializer):
    chickenId = serializers.SerializerMethodField()
    chickenSeedlingNumber = serializers.SerializerMethodField()
    chickenSeedlingAge = serializers.SerializerMethodField()
    incubationDate = serializers.SerializerMethodField()
    deathNumber = serializers.SerializerMethodField()
    eliminateNumber = serializers.SerializerMethodField()
    dataTime = serializers.SerializerMethodField()

    class Meta:
        model = ObituaryInfo
        fields = (
            "id", "chickenId", "chickenSeedlingNumber", "chickenSeedlingAge", "incubationDate", "deathNumber",
            "eliminateNumber", "dataTime")

    def get_chickenId(self, obj):
        return obj.chicken_flock_id

    def get_chickenSeedlingNumber(self, obj):
        return obj.chicken_seedling_number

    def get_chickenSeedlingAge(self, obj):
        return obj.chicken_seedling_age

    def get_incubationDate(self, obj):
        return obj.incubation_date

    def get_deathNumber(self, obj):
        return obj.death_number

    def get_eliminateNumber(self, obj):
        return obj.eliminate_number

    def get_dataTime(self, obj):
        return obj.data_time
