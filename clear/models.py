from django.db import models


class ClearProcedureInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="UUID")
    user_id = models.CharField(max_length=32, verbose_name="用户ID")
    period_validity = models.CharField(max_length=32, verbose_name="有效期")
    detergent = models.CharField(max_length=100, verbose_name="清洁剂")
    dentifrices = models.CharField(max_length=100, verbose_name="灭鼠剂")
    pesticide = models.CharField(max_length=100, verbose_name="杀虫剂")
    parasites_internal = models.CharField(max_length=100, verbose_name="内寄生虫杀虫剂")
    parasites_external = models.CharField(max_length=100, verbose_name="外寄生虫杀虫剂")
    data_time = models.CharField(max_length=10, verbose_name="数据时间")
    data_version = models.IntegerField(verbose_name="数据版本")
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        unique_together = (("id", "data_time", "data_version"),)
        db_table = "clear_procedure_info"
