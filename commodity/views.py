import json
import re



from commodity.models import CommodityInfo
from commodity.serializers import CommodityInfoSerializer

from rest_framework.decorators import api_view

from common.custom_page_params_verify import is_number, page_params_verify
from common.custon_page_conf.custom_page import CustomPagePagination
from common.token_utils import is_admin_users_login

from common.uuid_utils import get_uuid_str
from common.uuid_utils import get_default_id

from common.custom_response import ok
from common.custom_response import ok_page
from common.custom_response import error
from common.time_utils import get_format_time

from resources.models import ResourcesInfo


@api_view(['POST'])
def add(request):
    user_id = is_admin_users_login(request)
    if user_id is None:
        return error("沒有許可權")
    data = json.loads(request.body)
    if "name" not in data:
        return error("name 不能為空")
    if "type" not in data:
        return error("type 不能為空")
    if "resourcesId" not in data:
        return error("resources_id 不能為空")
    if "weight" not in data:
        return error("weight 不能為空")
    if "price" not in data:
        return error("price 不能為空")
    if not is_number(str(data["price"])):
        return error("price 格式不正確")
    if not is_number(str(data["weight"])):
        return error("weight 格式不正確")
    if int(data["weight"]) <= 0:
        return error("重量必须大于0")
    if float(data["price"]) <= 0:
        return error("价格必须大于0")
    price = int(float(data["price"]) * 100)
    weight = int(float(data["weight"]) * 1000)
    resources_info = ResourcesInfo.objects.filter(id=data["resourcesId"])
    if len(resources_info) == 0:
        return error("resources 不存在")

    CommodityInfo.objects.create(id=get_uuid_str(), shop_id=get_default_id(), name=data["name"],
                                 weight=weight,
                                 price=str(price),
                                 type=data["type"], number="0", resources_id=data["resourcesId"],
                                 remarks=data["remarks"],
                                 create_time=get_format_time(),
                                 create_by=user_id,
                                 update_time=get_format_time(),
                                 update_by=user_id,
                                 deleted='0',
                                 )
    return ok("新增成功")


@api_view(['POST'])
def query_page(request):
    if not page_params_verify(request) is None:
        return page_params_verify(request)
    sql = "select * from commodity_info where deleted = '0' "
    data = json.loads(request.body)
    if "type" in data:
        sql += " and type = '%s' " % data["type"]
    if "price" in data:
        sql += " and price = '%s' " % int(float(data["price"]) * 100)
    if "weight" in data:
        sql += " and weight = '%s' " % int(float(data["weight"]) * 1000)
    if "name" in data:
        # 代%的参数，只能如此拼接，否则会出现系统错误
        sql += " and `name` like '%%{0}%%' "
        sql = sql.format(data["name"])
    roles = CommodityInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = CommodityInfoSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)


@api_view(['GET'])
def delete(request, id):
    user_id = is_admin_users_login(request)
    if user_id is None:
        return error("沒有許可權")
    commodity_info = CommodityInfo.objects.filter(id=id).update(deleted='1')
    if commodity_info == 0:
        return error("待删除的数据不存在")
    else:
        return ok("删除成功")
