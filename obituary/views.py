import json

from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view

from chicken_flock.models import ChickenFlockInfo
from chicken_flock.serializers import ChickenFlockSerializer
from vmc_backend import settings
from .serializers import ObituaryInfoSerializer
from common.custom_page_params_verify import page_params_verify
from common.custom_response import error, ok, ok_page, ok_all_date
from common.custon_page_conf.custom_page import CustomPagePagination
from common.time_utils import get_format_time
from common.token_utils import is_ordinary_users_login, is_admin_users_login
from common.uuid_utils import get_uuid_str
from obituary.models import ObituaryInfo


# 获取最大版本数据
def get_mxa_version_data(user_id, chicken_id, data_time):
    sql = "SELECT t1.* FROM obituary_info t1 INNER JOIN ( SELECT t.user_id,t.id, MAX( t.data_version ) AS data_version FROM obituary_info t WHERE 1 = 1 and t.user_id = '%s' and deleted = '0'" % user_id
    if data_time is not None:
        sql += " and data_time  = '%s' " % data_time
    if chicken_id is not None:
        sql += " and chicken_flock_id  = '%s' " % chicken_id
    sql += " GROUP BY t.id  ) t2 ON t1.data_version = t2.data_version  	AND t1.id = t2.id and t1.user_id  = t2.user_id "
    roles = ObituaryInfo.objects.raw(sql)
    if len(roles) <= 0:
        return None
    return roles[0]


@api_view(['POST'])
def add(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)

    if "chickenId" not in data:
        return error("chickenId 不能為空")
    if "chickenSeedlingNumber" not in data:
        return error("chickenSeedlingNumber 不能為空")
    if "chickenSeedlingAge" not in data:
        return error("chickenSeedlingAge 不能為空")
    if "incubationDate" not in data:
        return error("incubationDate 不能為空")
    if "deathNumber" not in data:
        return error("deathNumber 不能為空")
    if "eliminateNumber" not in data:
        return error("eliminateNumber 不能為空")
    if "dataTime" not in data:
        return error("dataTime 不能為空")
    info = get_mxa_version_data(user_id, data["chickenId"], data["dataTime"])
    data_version = '0' if info is None else info.data_version
    # 修复: 始终生成新的UUID，而不是重用现有ID
    uuid = get_uuid_str()
    ObituaryInfo.objects.create(id=uuid, user_id=user_id, chicken_flock_id=data["chickenId"],
                                chicken_seedling_number=data["chickenSeedlingNumber"],
                                chicken_seedling_age=data["chickenSeedlingAge"],
                                incubation_date=data["incubationDate"],
                                death_number=data["deathNumber"],
                                eliminate_number=data["eliminateNumber"],
                                data_time=data["dataTime"],
                                data_version=int(data_version) + 1,
                                create_time=get_format_time(),
                                create_by=user_id,
                                update_time=get_format_time(),
                                update_by=user_id,
                                deleted='0',
                                )
    return ok("成功")


# 根据
def query_data(user_id, chicken_id, data_time):
    sql = "SELECT t1.* FROM obituary_info t1 INNER JOIN ( SELECT t.user_id,t.id, MAX( t.data_version ) AS data_version FROM obituary_info t WHERE 1 = 1 and t.user_id = '%s' and deleted = '0'" % user_id
    if data_time is not None:
        sql += " and data_time  = '%s' " % data_time
    if chicken_id is not None:
        sql += " and chicken_flock_id  = '%s' " % chicken_id
    sql += " GROUP BY t.id  ) t2 ON t1.data_version = t2.data_version  	AND t1.id = t2.id and t1.user_id  = t2.user_id "
    if settings.DEBUG:
        print("查询死淘率数据列表，执行SQL=[ %s ]" % sql)
    return ObituaryInfoSerializer(ObituaryInfo.objects.raw(sql), many=True).data


@api_view(['POST'])
def query_page(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    if not page_params_verify(request) is None:
        return page_params_verify(request)

    data = json.loads(request.body)

    # 1、需要查询到当前日期下 所有鸡群的死淘率
    # 1.1、分页查询当前用户鸡群信息

    sql = "SELECT t1.* FROM chicken_flock_info t1 INNER JOIN ( SELECT t.user_id, MAX( t.data_version ) AS data_version,t.id FROM chicken_flock_info t where 1 = 1  and t.user_id = '%s' and deleted = '0' " % user_id

    if "chickenId" in data:
        sql += " and  t.id = '%s' " % data["chickenId"]
    sql += " GROUP BY t.id ) t2 ON t1.data_version = t2.data_version  AND t1.user_id = t2.user_id and t1.id = t2.id"

    roles = ChickenFlockInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = ChickenFlockSerializer(page_roles, many=True)

    result = []
    for chicken in roles_ser.data:
        chicken_item = dict(chicken)
        # 1.2 查询当前日期下，每个鸡群的死淘率信息
        chicken_item["obituaryList"] = query_data(user_id, chicken["id"],
                                                  data["dataTime"] if "dataTime" in data else None)
        result.append(chicken_item)
    return ok_page(request, roles.__len__(), result)


@api_view(['POST'])
def query_date(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    sql = " SELECT * FROM obituary_info  WHERE  user_id = '%s' " % user_id
    if "chickenId" in data:
        sql += " and chicken_flock_id = '%s' " % data["chickenId"]
    sql += "GROUP BY DATA_TIME ORDER BY DATA_TIME DESC"
    roles = ObituaryInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = ObituaryInfoSerializer(page_roles, many=True)
    return ok_all_date(roles_ser.data)
