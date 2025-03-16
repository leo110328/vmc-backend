import json

from django.db.models import Q
from rest_framework.decorators import api_view

from common.custom_response import error, ok
from common.time_utils import get_format_time
from common.token_utils import is_ordinary_users_login
from common.uuid_utils import get_uuid_str
from dict_info.models import DictInfo
from dict_info.serializers import DictInfoSerializer


@api_view(['POST'])
def add(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "dictType" not in data:
        return error("dictType 不能為空")
    if "list" not in data:
        return error("list 不能為空")
    dicts = data["list"]
    if len(dicts) <= 0:
        return error("list 不能為空")
    # 先删除
    roles = DictInfo.objects.filter(Q(dict_type=data["dictType"]) & Q(user_id=user_id) & Q(deleted=0))
    roles.update(deleted="1")

    for item in dicts:
        DictInfo.objects.create(id=get_uuid_str(), user_id=user_id, dict_type=data["dictType"],
                                chinese_name=item["chineseName"],
                                english_name=item["englishName"],
                                create_time=get_format_time(),
                                create_by=user_id,
                                update_time=get_format_time(),
                                update_by=user_id,
                                deleted='0',
                                )
    return ok("成功")


@api_view(['POST'])
def query(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "dictType" in data:
        roles = DictInfo.objects.filter(Q(dict_type=data["dictType"]) & Q(deleted=0))
        roles_ser = DictInfoSerializer(roles, many=True)
        data = {"dictType": data["dictType"], "list": roles_ser.data}
        return ok([data])
    else:
        result = []
        sql = "select * from dict_info where deleted  = '0' GROUP BY dict_type "
        roles = DictInfo.objects.raw(sql)
        for item in roles:
            dict_type = item.dict_type
            result_item = DictInfo.objects.filter(Q(dict_type=dict_type) & Q(user_id=user_id) & Q(deleted=0))
            result_item_ser = DictInfoSerializer(result_item, many=True)
            data = {"dictType": dict_type, "list": result_item_ser.data}
            result.append(data)
        return ok(result)


@api_view(['POST'])
def delete(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "dictType" not in data:
        return error("dictType 不能為空")
    roles = DictInfo.objects.filter(Q(dict_type=data["dictType"]) & Q(deleted=0))
    if len(roles) <= 0:
        return error("数据不存在")
    roles.update(deleted="1")
    return ok("成功")
