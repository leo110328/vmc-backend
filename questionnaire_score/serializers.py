# serializers.py

from rest_framework import serializers
from .models import QuestionnaireScoreQueryInfo


class QuestionnaireScoreInfoSerializer(serializers.ModelSerializer):
    totalScore = serializers.SerializerMethodField()
    createTime = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = QuestionnaireScoreQueryInfo
        fields = ("id", "totalScore", "createTime", "userId", "nickname")

    def get_totalScore(self, obj):
        return obj.total_score

    def get_createTime(self, obj):
        return str(obj.create_time).split(" ")[0]

    def get_userId(self, obj):
        return obj.user_id

    def get_nickname(self, obj):
        return obj.username



