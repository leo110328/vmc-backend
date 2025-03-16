import json

from rest_framework.decorators import api_view
from django.db.models import Q
from commodity.models import CommodityInfo
from common.custom_page_params_verify import page_params_verify
from common.custom_response import ok, error, ok_page
from common.time_utils import get_format_time
from common.uuid_utils import get_uuid_str, get_default_id
from order.models import OrderInfo, OrderDetails
from order.serializers import OrderInfoSerializer, OrderDetailsSerializer
from common.custon_page_conf.custom_page import CustomPagePagination
from common.token_utils import is_ordinary_users_login, is_admin_users_login


# 获得订单商品总数
def get_order_commodity_number(datas):
    commodity_number = 0
    for data in datas:
        commodity_number += int(data["number"])
    return commodity_number


# 计算订单总价格
def get_total_price(commodity_info, datas):
    total_price = 0
    for commodity_info_item in commodity_info:
        price = commodity_info_item.price
        number = get_commodity_number(datas, commodity_info_item.pk)
        total_price += price * number
    return total_price


@api_view(['POST'])
def add(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    datas = []
    try:
        datas = json.loads(request.body.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        return error("请求数据参数异常")
    if len(datas) <= 0:
        return error("请求数据不能為空")
    # 验证请求参数格式是否正常
    for data in datas:
        if "commodityId" not in data or "number" not in data:
            return error("请求数据不能為空")
        if not str(data["number"]).isdigit():
            return error("请求数据参数异常")
        if int(data["number"]) <= 0:
            return error("number必须大于0")
    # 验证请求参数-商品是否存在，根据用户输入参数查询商品，查询得到的商品数和商品ID应该相等，如果不相等，说明传输的商品不存在
    query_parameter = Q()
    # 连接方式
    query_parameter.connector = 'OR'
    for data in datas:
        query_parameter.children.append(('id', data["commodityId"]))
    commodity_info = CommodityInfo.objects.filter(query_parameter)
    if len(commodity_info) != len(datas):
        return error("商品不存在")
    # 商品存在，生成订单信息和订单详细信息
    order_id = get_uuid_str()
    save_order(order_id, user_id, get_order_commodity_number(datas), get_total_price(commodity_info, datas), "1")
    for commodity_info_item in commodity_info:
        save_order_detail(order_id, user_id, get_commodity_number(datas, commodity_info_item.id),
                          commodity_info_item.id,
                          commodity_info_item.name, commodity_info_item.price, commodity_info_item.weight,
                          commodity_info_item.type,
                          commodity_info_item.resources_id)
    return ok({"orderId": order_id})


@api_view(['POST'])
def query_page(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    if not page_params_verify(request) is None:
        return page_params_verify(request)
    sql = " select * from order_info where 1 = 1 "
    user_id = is_admin_users_login(request)
    if user_id is None:
        sql += " and user_id = '%s' " % user_id
    data = json.loads(request.body)
    if "status" in data:
        sql += " and order_status = '%s' " % data["status"]
    if "id" in data:
        sql += " and id = '%s' " % data["id"]
    roles = OrderInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = OrderInfoSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)


# 删除订单
@api_view(['GET'])
def delete(request, id):
    user_id = is_admin_users_login(request)
    if user_id is None:
        return error("沒有許可權")
    order_info = OrderInfo.objects.filter(id=id)
    if len(order_info) == 0:
        return error("订单不存在")
    order_info.delete()
    return ok("操作成功")


@api_view(['POST'])
def update(request, id):
    user_id = is_admin_users_login(request)
    if user_id is None:
        return error("沒有許可權")
    data = json.loads(request.body)
    if not "status" in data:
        return error("status不能為空")
    order_info = OrderInfo.objects.filter(id=id)
    if len(order_info) == 0:
        return error("订单不存在")
    status = data["status"]
    if status not in ["2", "3", "4", "20"]:
        return error("订单状态异常")
    order_info.update(order_status=status)
    return ok("操作成功")


# 查询订单详细信息
@api_view(['GET'])
def detail(request, id):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    roles = OrderDetails.objects.filter(Q(order_id=id))
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = OrderDetailsSerializer(page_roles, many=True)
    return ok(roles_ser.data)


# 得到商品单价
def get_commodity_number(datas, commodity_id):
    for data in datas:
        if data["commodityId"] == commodity_id:
            return data["number"]
    return 0


# 保存订单
def save_order(uuid, user_id, number, total_price, order_status):
    OrderInfo.objects.create(id=uuid, user_id=user_id, number=number, total_price=total_price,
                             order_status=order_status,
                             create_time=get_format_time(),
                             order_time=get_format_time(),
                             create_by=user_id,
                             update_time=get_format_time(),
                             update_by=user_id,
                             deleted='0',
                             )


# 保存订单详细信息
def save_order_detail(order_id, user_id, number, commodity_id, name, price, weight, type, resources_id):
    OrderDetails.objects.create(id=get_uuid_str(), order_id=order_id, user_id=user_id,
                                commodity_id=commodity_id,
                                name=name,
                                price=price,
                                weight=weight,
                                type=type,
                                number=number,
                                resources_id=resources_id,
                                create_time=get_format_time(),
                                create_by=user_id,
                                update_time=get_format_time(),
                                update_by=user_id,
                                deleted='0',
                                )
