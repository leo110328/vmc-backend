from django.db import models


# 普通饲料管理
class FineFeedDosageInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="UUID")
    user_id = models.CharField(max_length=32, verbose_name="用户ID")
    chicken_seed_fine_feed_dosage = models.CharField(max_length=32, verbose_name="每月鸡苗精料用量")
    chicken_develop_fine_feed_dosage = models.CharField(max_length=32, verbose_name="每月中鸡精料用量")
    chicken_mature_fine_feed_dosage = models.CharField(max_length=32, verbose_name="每月大鸡精料用量")
    chicken_laying_hens_fine_feed_dosage = models.CharField(max_length=32, verbose_name="每月下单母鸡精料用量")
    chicken_later_borrowing_fine_feed_dosage = models.CharField(max_length=32, verbose_name="每月後借母鸡精料用量")
    chicken_cock_fine_feed_dosage = models.CharField(max_length=32, verbose_name="每月公鸡精料用量")
    data_time = models.CharField(max_length=10, verbose_name="数据时间")
    data_version = models.IntegerField(verbose_name="数据版本")
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        unique_together = (("id", "data_time", "data_version"),)
        db_table = "fine_feed_dosage_info"
