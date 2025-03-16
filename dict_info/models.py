from django.db import models


class DictInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True,
                          verbose_name="UUID")
    user_id = models.CharField(max_length=32, verbose_name="用户ID")
    dict_type = models.CharField(max_length=32, verbose_name="类型")
    chinese_name = models.TextField(max_length=10000, verbose_name="中文名称")
    english_name = models.CharField(max_length=100, verbose_name="英文名称")
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        unique_together = ("id",)
        db_table = "dict_info"
