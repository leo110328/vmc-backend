from django.db import models


# 问卷得分
class QuestionnaireScoreInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="数据ID")
    farm_id = models.CharField(max_length=32, verbose_name="农场ID,问卷归属人ID")
    user_id = models.CharField(max_length=32, verbose_name="用户ID,答题人ID")
    total_score = models.IntegerField(verbose_name="总得分")
    data_version = models.IntegerField(verbose_name="数据版本")
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")
    class Meta:
        db_table = "questionnaire_score_info"


class QuestionnaireScoreQueryInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="数据ID")
    farm_id = models.CharField(max_length=32, verbose_name="农场ID,问卷归属人ID")
    user_id = models.CharField(max_length=32, verbose_name="用户ID,答题人ID")
    username = models.CharField(max_length=32,
                                verbose_name="用户名称,答题人账号,数据库没有对应键,sql进行查询")
    total_score = models.IntegerField(verbose_name="总得分")
    data_version = models.IntegerField(verbose_name="数据版本")
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")
