import json
from django.db import connection
from django.core.serializers import serialize
from django.db.models import Q

from rest_framework.decorators import api_view

from common.custom_page_params_verify import page_params_verify
from common.custon_page_conf.custom_page import CustomPagePagination

from commodity.models import CommodityInfo
from common.token_utils import is_ordinary_users_login
from shopp_cart.serializers import ShoppCartInfoSerializer
from common.custom_response import ok, error, ok_page
from common.time_utils import get_format_time
from common.uuid_utils import get_uuid_str, get_default_id

from shopp_cart.models import ShoppCartInfo


@api_view(['POST'])
def add_commodity(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "commodityId" not in data:
        return error("commodityId 不能為空")
    commodity_info = CommodityInfo.objects.filter(id=data["commodityId"])
    if len(commodity_info) == 0:
        return error("商品不存在")
    add_number = 1
    if "number" in data:
        add_number = data["number"]
        if int(add_number) <= 0 or int(add_number) > 99:
            return error("商品数量必须在1-99之间")
    shopp_cart_info = ShoppCartInfo.objects.filter(Q(commodity_id=data["commodityId"]) & Q(user_id=user_id))
    if len(shopp_cart_info) == 0:
        save_shopp_cart(user_id, data["commodityId"], int(add_number))
    else:
        number = json.loads(serialize('json', shopp_cart_info))[0]["fields"]["number"]
        shopp_cart_info.update(number=int(number) + int(add_number))
    return ok("操作成功")


@api_view(['POST'])
def delete_commodity(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "commodityId" not in data:
        return error("commodityId 不能為空")
    shopp_cart_info = ShoppCartInfo.objects.filter(Q(commodity_id=data["commodityId"]) & Q(user_id=user_id))
    if len(shopp_cart_info) == 0:
        return error("商品不存在")
    else:
        number = int(json.loads(serialize('json', shopp_cart_info))[0]["fields"]["number"])
        if number > 1:
            shopp_cart_info.update(number=number - 1)
        else:
            shopp_cart_info.delete()
    return ok("操作成功")


@api_view(['POST'])
def clear_commodity(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")

    data = json.loads(request.body)
    if "commodityId" not in data:
        return error("commodityId 不能為空")
    shopp_cart_info = ShoppCartInfo.objects.filter(Q(commodity_id=data["commodityId"]) & Q(user_id=user_id))
    if len(shopp_cart_info) == 0:
        return error("商品不存在")
    else:
        shopp_cart_info.delete()
    return ok("操作成功")


@api_view(['POST'])
def clear_cart(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    shopp_cart_info = ShoppCartInfo.objects.filter(Q(user_id=user_id)).delete()
    return ok("操作成功")


@api_view(['POST'])
def clear_commodity(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "commodityId" not in data:
        return error("commodityId 不能為空")
    shopp_cart_info = ShoppCartInfo.objects.filter(Q(commodity_id=data["commodityId"]) & Q(user_id=user_id))
    if len(shopp_cart_info) == 0:
        return error("商品不存在")
    else:
        shopp_cart_info.delete()
    return ok("操作成功")


@api_view(['POST'])
def query_page(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    if not page_params_verify(request) is None:
        return page_params_verify(request)
    roles = []
    with connection.cursor() as cursor:
        cursor.execute(
            "select b.id,b.name,b.price,b.resources_id,b.remarks,b.type,a.number from shopp_cart_info a join commodity_info b on a.commodity_id = b.id  where a.user_id =  %s",
            [user_id])
        roles = cursor.fetchall()
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    result = []
    for role in page_roles:
        item = {"id": role[0], "name": role[1], "price": role[2] / 100, "image": role[3], "remarks": role[4],
                "type": role[5],
                "number": role[6]}
        result.append(item)
    return ok_page(request, roles.__len__(), result)


def save_shopp_cart(user_id, commodity_id, number):
    ShoppCartInfo.objects.create(id=get_uuid_str(), user_id=user_id, commodity_id=commodity_id, number=number,
                                 create_time=get_format_time(),
                                 create_by=user_id,
                                 update_time=get_format_time(),
                                 update_by=user_id,
                                 deleted='0',
                                 )
