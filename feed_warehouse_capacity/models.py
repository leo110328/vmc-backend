from django.db import models


class FeedWarehouseCapacityInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="UUID")
    user_id = models.CharField(max_length=32, verbose_name="用户ID")
    mixed_feed_frequency = models.CharField(max_length=32, verbose_name="每月混合饲料次数")
    mixed_feed_containers_frequency = models.CharField(max_length=32, verbose_name="饲料混合器数量")
    chicken_seed_mixed_feed_containers_frequency = models.CharField(max_length=100, verbose_name="鸡苗饲料混合器数量")
    chicken_develop_mixed_feed_containers_frequency = models.CharField(max_length=100,
                                                                       verbose_name="中雞至大雞飼料混合器容量")
    chicken_mature_mixed_feed_containers_frequency = models.CharField(max_length=100, verbose_name="大雞飼料混合器容量")
    feed_tower_capacity = models.CharField(max_length=100, verbose_name="料塔容量")
    feed_tower_number = models.CharField(max_length=100, verbose_name="料塔数量")
    mixed_feed_clear_number = models.CharField(max_length=100, verbose_name="每月饲料混合器清理数量")
    feed_tower_clear_number = models.CharField(max_length=100, verbose_name="每月料塔清理数量")
    data_time = models.CharField(max_length=10, verbose_name="数据时间")
    data_version = models.IntegerField(verbose_name="数据版本")
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        unique_together = (("id", "data_time", "data_version"),)
        db_table = "feed_warehouse_capacity_info"
