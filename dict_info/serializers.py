# serializers.py

from rest_framework import serializers

from dict_info.models import DictInfo


class DictInfoSerializer(serializers.ModelSerializer):
    chineseName = serializers.SerializerMethodField()
    englishName = serializers.SerializerMethodField()

    class Meta:
        model = DictInfo
        fields = ("chineseName", "englishName")


    def get_chineseName(self, obj):
        return obj.chinese_name

    def get_englishName(self, obj):
        return obj.english_name
