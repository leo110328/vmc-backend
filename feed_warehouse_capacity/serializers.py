# serializers.py

from rest_framework import serializers
from .models import FeedWarehouseCapacityInfo


class FeedWarehouseCapacityInfoSerializer(serializers.ModelSerializer):
    mixedFeedFrequency = serializers.SerializerMethodField()
    mixedFeedContainersFrequency = serializers.SerializerMethodField()
    chickenSeedMixedFeedContainersFrequency = serializers.SerializerMethodField()
    chickenDevelopMixedFeedContainersFrequency = serializers.SerializerMethodField()
    chickenMatureMixedFeedContainersFrequency = serializers.SerializerMethodField()
    feedTowerCapacity = serializers.SerializerMethodField()
    feedTowerNumber = serializers.SerializerMethodField()
    mixedFeedClearNumber = serializers.SerializerMethodField()
    feedTowerClearNumber = serializers.SerializerMethodField()
    dataTime = serializers.SerializerMethodField()

    class Meta:
        model = FeedWarehouseCapacityInfo
        fields = ("id", "mixedFeedFrequency", "mixedFeedContainersFrequency", "chickenSeedMixedFeedContainersFrequency",
                  "chickenDevelopMixedFeedContainersFrequency", "chickenMatureMixedFeedContainersFrequency",
                  "feedTowerCapacity", "feedTowerNumber", "mixedFeedClearNumber", "feedTowerClearNumber", "dataTime")

    def get_mixedFeedFrequency(self, obj):
        return obj.mixed_feed_frequency

    def get_mixedFeedContainersFrequency(self, obj):
        return obj.mixed_feed_containers_frequency

    def get_chickenSeedMixedFeedContainersFrequency(self, obj):
        return obj.chicken_seed_mixed_feed_containers_frequency

    def get_chickenDevelopMixedFeedContainersFrequency(self, obj):
        return obj.chicken_develop_mixed_feed_containers_frequency

    def get_chickenMatureMixedFeedContainersFrequency(self, obj):
        return obj.chicken_mature_mixed_feed_containers_frequency

    def get_feedTowerCapacity(self, obj):
        return obj.feed_tower_capacity

    def get_feedTowerNumber(self, obj):
        return obj.feed_tower_number

    def get_mixedFeedClearNumber(self, obj):
        return obj.mixed_feed_clear_number

    def get_feedTowerClearNumber(self, obj):
        return obj.feed_tower_clear_number

    def get_dataTime(self, obj):
        return obj.data_time
