# serializers.py

from rest_framework import serializers
from .models import CommodityInfo


class CommodityInfoSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()

    class Meta:
        model = CommodityInfo
        fields = ("id", "name", "price", "image", "remarks", "weight")

    def get_price(self, obj):
        return obj.price / 100

    def get_weight(self, obj):
        return obj.weight / 100

    def get_image(self, obj):
        return obj.resources_id

    def get_publish(self, obj):
        return {'id': obj.name, 'name': obj.name}
