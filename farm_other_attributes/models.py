from django.db import models


class FarmOtherAttributesInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="UUID")
    user_id = models.CharField(max_length=32, verbose_name="用户ID")
    farm_id = models.CharField(max_length=32, verbose_name="农场ID")
    sensitive = models.CharField(max_length=5000, verbose_name="敏感性")
    intermediate = models.CharField(max_length=255, verbose_name="中间性")
    resistant = models.CharField(max_length=255, verbose_name="抵抗性")
    antibiotic = models.CharField(max_length=255, verbose_name="抗生素")
    bacterial_type = models.CharField(max_length=255, verbose_name="菌类")
    data_time = models.CharField(max_length=10, verbose_name="数据时间")
    data_version = models.IntegerField(verbose_name="数据版本")
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        unique_together = (("id", "data_time", "data_version"),)
        db_table = "farm_other_attributes_info"
