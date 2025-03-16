# serializers.py

from rest_framework import serializers
from .models import FineFeedDosageInfo


class FineFeedDosageInfoSerializer(serializers.ModelSerializer):
    chickenSeedFineFeedDosage = serializers.SerializerMethodField()
    chickenDevelopFineFeedDosage = serializers.SerializerMethodField()
    chickenMatureFineFeedDosage = serializers.SerializerMethodField()
    chickenLayingHensFineFeedDosage = serializers.SerializerMethodField()
    chickenLaterBorrowingFineFeedDosage = serializers.SerializerMethodField()
    chickenCockFineFeedDosage = serializers.SerializerMethodField()
    dataTime = serializers.SerializerMethodField()

    class Meta:
        model = FineFeedDosageInfo
        fields = (
            "id", "dataTime", "chickenSeedFineFeedDosage", "chickenDevelopFineFeedDosage",
            "chickenMatureFineFeedDosage",
            "chickenLayingHensFineFeedDosage", "chickenLaterBorrowingFineFeedDosage", "chickenCockFineFeedDosage")

    def get_chickenSeedFineFeedDosage(self, obj):
        return obj.chicken_seed_fine_feed_dosage

    def get_chickenDevelopFineFeedDosage(self, obj):
        return obj.chicken_develop_fine_feed_dosage

    def get_chickenMatureFineFeedDosage(self, obj):
        return obj.chicken_mature_fine_feed_dosage

    def get_chickenLayingHensFineFeedDosage(self, obj):
        return obj.chicken_laying_hens_fine_feed_dosage

    def get_chickenLaterBorrowingFineFeedDosage(self, obj):
        return obj.chicken_later_borrowing_fine_feed_dosage

    def get_chickenCockFineFeedDosage(self, obj):
        return obj.chicken_cock_fine_feed_dosage

    def get_dataTime(self, obj):
        return obj.data_time
