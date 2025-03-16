# serializers.py

from rest_framework import serializers
from .models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    farmName = serializers.SerializerMethodField()
    admin = serializers.SerializerMethodField()

    class Meta:
        model = UserInfo
        fields = ("id", "username", "email", "phone", "farmName", "admin")

    def get_farmName(self, obj):
        return obj.farm_name

    def get_admin(self, obj):
        return obj.is_admin
