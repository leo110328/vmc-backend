# serializers.py

from rest_framework import serializers
from .models import NoticeInfo


class NoticeInfoSerializer(serializers.ModelSerializer):
    msgTime = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    # status = serializers.SerializerMethodField()

    class Meta:
        model = NoticeInfo
        fields = ("id", "title", "text", "image", "msgTime")

    def get_msgTime(self, obj):
        return obj.msg_time

    def get_image(self, obj):
        return obj.resources_id
