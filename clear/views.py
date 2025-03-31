import json

from django.db.models import Q
from rest_framework.decorators import api_view

from clear.models import ClearProcedureInfo
from clear.serializers import ClearProcedureInfoSerializer
from common.custom_page_params_verify import page_params_verify
from common.custom_response import error, ok, ok_page, ok_all_date
from common.custon_page_conf.custom_page import CustomPagePagination
from common.time_utils import get_format_time
from common.token_utils import is_ordinary_users_login, is_admin_users_login
from common.uuid_utils import get_uuid_str
from vmc_backend import settings


# Create your views here.

# 获取最大版本数据
def get_mxa_version_data(user_id, date_time):
    sql = " SELECT t1.* FROM clear_procedure_info t1 INNER JOIN ( SELECT t.user_id, t.data_time,MAX( t.data_version ) AS data_version FROM clear_procedure_info t where 1 = 1 and t.user_id = '%s' " % user_id
    if date_time is not None:
        sql += "and data_time = '%s' " % date_time
    sql += " and deleted = '0' GROUP BY data_time  ) t2 ON t1.data_version = t2.data_version  	AND t1.data_time = t2.data_time  AND t1.user_id = t2.user_id"
    if settings.DEBUG:
        print("查询查询清理数据最大版本数据，执行SQL=[ %s ]" % sql)
    roles = ClearProcedureInfo.objects.raw(sql)
    if len(roles) <= 0:
        return None
    return roles[0]


@api_view(['POST'])
def add(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "dataTime" not in data:
        return error("时间 不能為空")
    if "periodValidity" not in data:
        return error("有效期 不能為空")
    if "detergent" not in data:
        return error("清洁剂 不能為空")
    if "dentifrices" not in data:
        return error("灭鼠剂 不能為空")
    if "pesticide" not in data:
        return error("杀虫剂 不能為空")
    if "parasitesInternal" not in data:
        return error("内寄生虫杀虫剂 不能為空")
    if "parasitesExternal" not in data:
        return error("外寄生虫杀虫剂 不能為空")
    info = get_mxa_version_data(user_id, data["dataTime"])
    data_version = '0' if info is None else info.data_version
    # 修复: 始终生成新的UUID，而不是重用现有ID
    uuid = get_uuid_str()
    ClearProcedureInfo.objects.create(id=uuid, user_id=user_id, period_validity=data["periodValidity"],
                                      detergent=data["detergent"],
                                      dentifrices=data["dentifrices"],
                                      pesticide=data["pesticide"],
                                      parasites_internal=data["parasitesInternal"],
                                      parasites_external=data["parasitesExternal"],
                                      data_time=data["dataTime"],
                                      data_version=int(data_version) + 1,
                                      create_time=get_format_time(),
                                      create_by=user_id,
                                      update_time=get_format_time(),
                                      update_by=user_id,
                                      deleted='0',
                                      )
    return ok("成功")


@api_view(['POST'])
def delete(request, id):
    user_id = is_admin_users_login(request)
    if user_id is None:
        return error("未登錄")
    roles = ClearProcedureInfo.objects.filter(Q(id=id))
    if len(roles) <= 0:
        return error("数据不存在")
    roles.update(deleted="1")
    return ok("成功")


@api_view(['POST'])
def query_page(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    if not page_params_verify(request) is None:
        return page_params_verify(request)

    data = json.loads(request.body)
    sql = " SELECT t1.* FROM clear_procedure_info t1 INNER JOIN ( SELECT t.user_id, t.data_time,MAX( t.data_version ) AS data_version FROM clear_procedure_info t where 1 = 1 and t.user_id = '%s' " % user_id
    if "dataTime" in data:
        sql += "and data_time = '%s' " % data["dataTime"]
    sql += " and deleted = '0' GROUP BY data_time  ) t2 ON t1.data_version = t2.data_version  	AND t1.data_time = t2.data_time  AND t1.user_id = t2.user_id"
    if settings.DEBUG:
        print("查询清理数据，执行SQL=[ %s ]" % sql)

    roles = ClearProcedureInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = ClearProcedureInfoSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)


@api_view(['GET'])
def query_date(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    sql = " SELECT * FROM clear_procedure_info  WHERE  user_id = '%s'  GROUP BY DATA_TIME ORDER BY DATA_TIME DESC " % user_id
    roles = ClearProcedureInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = ClearProcedureInfoSerializer(page_roles, many=True)
    return ok_all_date(roles_ser.data)
