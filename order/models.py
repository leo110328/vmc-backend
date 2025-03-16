from django.db import models


class OrderInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="UUID")
    user_id = models.CharField(max_length=32, verbose_name="用户ID")
    number = models.IntegerField(verbose_name="商品数量", null=True, blank=True)
    total_price = models.IntegerField(verbose_name="订单总价,单位分")
    order_status = models.CharField(max_length=2,
                                    verbose_name="订单状态[0:未下单,1:已下单,2:已付款,3:已发货,4:已收货,20:订单正常完成,21:订单超时完成,22:订单已取消]")
    order_time = models.CharField(max_length=50, verbose_name="下单时间")
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        db_table = "order_info"


class OrderDetails(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="UUID")
    order_id = models.CharField(max_length=32, verbose_name="订单ID")
    user_id = models.CharField(max_length=32, verbose_name="用户ID")
    commodity_id = models.CharField(max_length=32, verbose_name="商品ID")
    name = models.TextField(verbose_name="商品名称")
    price = models.IntegerField(verbose_name="商品单价,单位分")
    type = models.CharField(max_length=1, verbose_name="商品类型", null=True, blank=True)
    number = models.IntegerField(verbose_name="商品数量", null=True, blank=True)
    weight = models.IntegerField(verbose_name="商品重量", null=True, blank=True)
    resources_id = models.CharField(max_length=32, verbose_name="资源ID", null=True, blank=True)
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        db_table = "order_details"
