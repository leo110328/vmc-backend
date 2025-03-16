# serializers.py

from rest_framework import serializers
from .models import OrderInfo, OrderDetails


class OrderInfoSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = OrderInfo
        fields = ("id", "price", "status")

    def get_price(self, obj):
        return obj.total_price / 100

    def get_status(self, obj):
        if obj.order_status == "0":
            return "未下单"
        if obj.order_status == "1":
            return "未付款"
        if obj.order_status == "2":
            return "已付款"
        if obj.order_status == "3":
            return "已发货"
        if obj.order_status == "4":
            return "已收货"
        if obj.order_status == "20":
            return "订单正常完成"
        if obj.order_status == "21":
            return "订单超时完成"
        if obj.order_status == "22":
            return "订单已取消"


class OrderDetailsSerializer(serializers.ModelSerializer):
    orderId = serializers.SerializerMethodField()
    commodityId = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    # status = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetails
        fields = ("id", "orderId", "commodityId", "name", "price", "type", "number", "images", "weight")
        # fields = "__all__"

    def get_weight(self, obj):
        return obj.weight / 1000

    def get_price(self, obj):
        return obj.price / 100

    def get_orderId(self, obj):
        return obj.order_id

    def get_commodityId(self, obj):
        return obj.commodity_id

    def get_images(self, obj):
        return obj.resources_id

    def get_type(self, obj):
        if obj.type == "0":
            return "口服"
        if obj.type == "1":
            return "疫苗"
