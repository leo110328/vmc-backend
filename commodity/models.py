from django.db import models


class CommodityInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="UUID")
    shop_id = models.CharField(max_length=32, verbose_name="店铺ID", null=True, blank=True)
    name = models.TextField(verbose_name="商品名称")
    price = models.IntegerField(verbose_name="商品单价,单位分")
    weight = models.IntegerField(verbose_name="商品重量,单位分")
    type = models.CharField(max_length=1, verbose_name="商品类型", null=True, blank=True)
    number = models.CharField(max_length=1, verbose_name="商品数量", null=True, blank=True)
    resources_id = models.CharField(max_length=32, verbose_name="资源ID", null=True, blank=True)
    remarks = models.TextField(verbose_name="备注", null=True, blank=True)
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        db_table = "commodity_info"
