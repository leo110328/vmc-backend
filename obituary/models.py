from django.db import models


# 鸡群死亡和淘汰数据
class ObituaryInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="UUID")
    user_id = models.CharField(max_length=32, verbose_name="用户ID")
    chicken_flock_id = models.CharField(max_length=32, verbose_name="鸡群ID")
    chicken_seedling_number = models.CharField(max_length=255, verbose_name="鸡苗数量")
    chicken_seedling_age = models.CharField(max_length=255, verbose_name="鸡苗年龄")
    incubation_date = models.CharField(max_length=255, verbose_name="孵化日期")
    death_number = models.CharField(max_length=255, verbose_name="死亡数量")
    eliminate_number = models.CharField(max_length=255, verbose_name="淘汰数量")
    data_time = models.CharField(max_length=10, verbose_name="数据时间")
    data_version = models.IntegerField(verbose_name="数据版本")
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        unique_together = (("id", "data_time", "data_version"),)
        db_table = "obituary_info"
