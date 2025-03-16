from django.db import models


class FarmHomeInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True,
                          verbose_name="UUID,一条数据有多个版本，和data_version共同组成一份唯一数据")
    user_id = models.CharField(max_length=32, verbose_name="用户ID")
    breeding_quota = models.CharField(max_length=32, verbose_name="养殖额度")
    chicken_seedlings_type = models.TextField(max_length=10000, verbose_name="鸡苗种类")
    breeding_methods = models.CharField(max_length=100, verbose_name="养殖方式")
    chicken_seedlings_number1 = models.CharField(max_length=100, verbose_name="鸡苗数量1")
    chicken_seedlings_number2 = models.CharField(max_length=100, verbose_name="鸡苗数量2")
    chicken_seedlings_number3 = models.CharField(max_length=100, verbose_name="鸡苗数量3")
    chicken_seedlings_volume1 = models.CharField(max_length=100, verbose_name="鸡苗体积1")
    chicken_seedlings_volume2 = models.CharField(max_length=100, verbose_name="鸡苗体积2")
    chicken_seedlings_volume3 = models.CharField(max_length=100, verbose_name="鸡苗体积3")
    data_version = models.CharField(max_length=3, verbose_name="数据版本")
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        unique_together = (("id", "data_version"),)
        db_table = "farm_home_info"
