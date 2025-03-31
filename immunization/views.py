import json

from django.db.models import Q
from rest_framework.decorators import api_view

from common.custom_page_params_verify import page_params_verify
from common.custom_response import error, ok, ok_page, ok_all_date
from common.custon_page_conf.custom_page import CustomPagePagination
from common.time_utils import get_format_time
from common.token_utils import is_ordinary_users_login, is_admin_users_login
from common.uuid_utils import get_uuid_str
from immunization.models import ImmunizationInfo
from immunization.serializers import ImmunizationInfoSerializer
from vmc_backend import settings


# Create your views here.


# 获取最大版本数据
def get_mxa_version_data(user_id, date_time):
    # 查询当前用户最大版本数据
    sql = " SELECT t1.* FROM immunization_info t1 INNER JOIN ( SELECT t.user_id, t.data_time,MAX( t.data_version ) AS data_version FROM immunization_info t where 1 = 1 and t.user_id = '%s' " % user_id
    if date_time is not None:
        sql += "and data_time = '%s' " % date_time
    sql += " and deleted = '0' GROUP BY data_time  ) t2 ON t1.data_version = t2.data_version  	AND t1.data_time = t2.data_time  AND t1.user_id = t2.user_id"
    if settings.DEBUG:
        print("查询养殖记录最大版本数据，执行SQL=[ %s ]" % sql)
    roles = ImmunizationInfo.objects.raw(sql)
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
    if "vaccineName" not in data:
        return error("疫苗名称 不能為空")
    if "vaccineType" not in data:
        return error("疫苗毒株 不能為空")
    if "vaccineDate" not in data:
        return error("疫苗接种日期 不能為空")
    if "vaccineFrequency" not in data:
        return error("疫苗接种次数 不能為空")
    if "vaccineDosage" not in data:
        return error("疫苗接种剂量 不能為空")
    if "vaccineRoute" not in data:
        return error("疫苗批次 不能為空")
    if "vaccineManufacturers" not in data:
        return error("疫苗制造商 不能為空")
    if "vaccineAddress" not in data:
        return error("疫苗制造地 不能為空")
    info = get_mxa_version_data(user_id, data["dataTime"])
    data_version = '0' if info is None else info.data_version
    
    # 修复：始终生成新的UUID，不重用现有ID
    uuid = get_uuid_str()
    
    ImmunizationInfo.objects.create(id=uuid, user_id=user_id, period_validity=data["periodValidity"],
                                    vaccine_name=data["vaccineName"],
                                    vaccine_type=data["vaccineType"],
                                    vaccine_batch=data["vaccineBatch"],
                                    vaccine_date=data["vaccineDate"],
                                    vaccine_frequency=data["vaccineFrequency"],
                                    vaccine_dosage=data["vaccineDosage"],
                                    vaccine_route=data["vaccineRoute"],
                                    vaccine_manufacturers=data["vaccineManufacturers"],
                                    vaccine_address=data["vaccineAddress"],
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
    roles = ImmunizationInfo.objects.filter(Q(id=id))
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

    sql = " SELECT t1.* FROM immunization_info t1 INNER JOIN ( SELECT t.user_id, t.data_time,MAX( t.data_version ) AS data_version FROM immunization_info t where 1 = 1 and t.user_id = '%s' " % user_id
    if "dataTime" in data:
        sql += "and data_time = '%s' " % data["dataTime"]
    sql += " and deleted = '0' GROUP BY data_time  ) t2 ON t1.data_version = t2.data_version  	AND t1.data_time = t2.data_time  AND t1.user_id = t2.user_id"
    if settings.DEBUG:
        print("查询养殖记录数据，执行SQL=[ %s ]" % sql)

    roles = ImmunizationInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = ImmunizationInfoSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)


@api_view(['GET'])
def query_date(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    sql = " SELECT * FROM immunization_info  WHERE  user_id = '%s'  GROUP BY data_time ORDER BY data_time DESC " % user_id
    roles = ImmunizationInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = ImmunizationInfoSerializer(page_roles, many=True)
    return ok_all_date(roles_ser.data)
