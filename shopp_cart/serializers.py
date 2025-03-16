# serializers.py

from rest_framework import serializers
from .models import ShoppCartInfo


class ShoppCartInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppCartInfo
        # fields = ("commodity_id", "number")
        fields = "__all__"
