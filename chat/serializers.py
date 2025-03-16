# serializers.py
import time

from rest_framework import serializers
from .models import MsgInfo


class MsgInfoSerializer(serializers.ModelSerializer):
    sendTime = serializers.SerializerMethodField()
    sendId = serializers.SerializerMethodField()
    acceptId = serializers.SerializerMethodField()
    msgId = serializers.SerializerMethodField()
    msgValue = serializers.SerializerMethodField()
    sendName = serializers.SerializerMethodField()

    class Meta:
        model = MsgInfo
        fields = ("sendId", "acceptId", "msgId", "msgValue", "sendTime", "sendName")

    def get_sendTime(self, obj):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(obj.timestamp)))

    def get_sendId(self, obj):
        return obj.send_id

    def get_sendName(self, obj):
        return obj.send_name

    def get_acceptId(self, obj):
        return obj.accept_id

    def get_msgId(self, obj):
        return obj.msg_id

    def get_msgValue(self, obj):
        return obj.msg_value
