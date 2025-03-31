import json

from django.db.models import Q
from rest_framework.decorators import api_view

from common.custom_page_params_verify import page_params_verify
from common.custom_response import error, ok, ok_page, ok_all_date
from common.custon_page_conf.custom_page import CustomPagePagination
from common.time_utils import get_format_time
from common.token_utils import is_ordinary_users_login, is_admin_users_login
from common.uuid_utils import get_uuid_str
from farm_other_attributes.models import FarmOtherAttributesInfo
from farm_other_attributes.serializers import FarmOtherAttributesSerializer
from user.models import UserInfo
from user.serializers import UserInfoSerializer
from vmc_backend import settings


# Create your views here.


# 获取最大版本数据
def get_mxa_version_data(farm_id, date_time,data):
    # 查询当前用户最大版本数据
    sql = " SELECT t1.* FROM farm_other_attributes_info t1 INNER JOIN ( SELECT t.farm_id, t.data_time,MAX( t.data_version ) AS data_version FROM farm_other_attributes_info t where 1 = 1 and t.farm_id = '%s' " % farm_id
    if date_time is not None:
        sql += "and data_time = '%s' " % date_time
    if "antibiotic"  in data:
        sql += "and antibiotic = '%s' " % data['antibiotic']
    if "bacterialType"  in data:
        sql += "and bacterial_type = '%s' " % data['bacterialType']
    sql += " and deleted = '0' GROUP BY data_time  ) t2 ON t1.data_version = t2.data_version  	AND t1.data_time = t2.data_time  AND t1.farm_id = t2.farm_id"
    if settings.DEBUG:
        print("查询农场其他信息最大数据版本，执行SQL=[ %s ]" % sql)
    roles = FarmOtherAttributesInfo.objects.raw(sql)
    if len(roles) <= 0:
        return None
    return roles[0]


@api_view(['POST'])
def add(request):
    user_id = is_admin_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "dataTime" not in data:
        return error("时间 不能為空")
    if "farmId" not in data:
        return error("farmId 不能為空")
    if "sensitive" not in data:
        return error("sensitive 不能為空")
    if "intermediate" not in data:
        return error("intermediate 不能為空")
    if "resistant" not in data:
        return error("resistant 不能為空")
    if "antibiotic" not in data:
        return error("antibiotic 不能為空")
    if "bacterialType" not in data:
        return error("bacterialType 不能為空")

    query_farm_sql = "select * from user_info where deleted = '0' and id = '{}' "
    roles = UserInfo.objects.raw(query_farm_sql.format(data["farmId"]))
    if len(roles) <= 0:
        return error("farmId不存在")

    info = get_mxa_version_data(data["farmId"], data["dataTime"],data)
    data_version = '0' if info is None else info.data_version
    # 修复: 始终生成新的UUID，而不是重用现有ID
    uuid = get_uuid_str()
    FarmOtherAttributesInfo.objects.create(id=uuid, user_id=user_id, farm_id=data["farmId"],
                                           sensitive=data["sensitive"],
                                           intermediate=data["intermediate"],
                                           resistant=data["resistant"],
                                           data_time=data["dataTime"],
                                           antibiotic=data["antibiotic"],
                                           bacterial_type=data["bacterialType"],
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
    roles = FarmOtherAttributesInfo.objects.filter(Q(id=id))
    if len(roles) <= 0:
        return error("数据不存在")
    roles.update(deleted="1")
    return ok("成功")


# 查找其他信息
def getFarmOtherAttributes(farm_id, farm_name, data):
    sql = " SELECT t1.* FROM farm_other_attributes_info t1 INNER JOIN ( SELECT t.farm_id, t.data_time,MAX( t.data_version ) AS data_version FROM farm_other_attributes_info t where 1 = 1 and t.farm_id = '%s' " % farm_id
    if "sensitive" in data:
        sql += " AND t.sensitive = '%s' " % data["sensitive"]
    if "intermediate" in data:
        sql += " AND t.intermediate = '%s' " % data["intermediate"]
    if "resistant" in data:
        sql += " AND t.resistant = '%s' " % data["resistant"]
    if "dataTime" in data:
        sql += " AND t.data_time = '%s' " % data["dataTime"]
    if "antibiotic" in data:
        sql += " AND t.antibiotic = '%s' " % data["antibiotic"]
    if "bacterialType" in data:
        sql += " AND t.bacterial_type = '%s' " % data["bacterialType"]
    sql += " and deleted = '0' GROUP BY data_time  ) t2 ON t1.data_version = t2.data_version  	AND t1.data_time = t2.data_time  AND t1.farm_id = t2.farm_id"
    if settings.DEBUG:
        print("查询农场其他信息列表，执行SQL=[ %s ]" % sql)
    roles = FarmOtherAttributesInfo.objects.raw(sql)
    farmOtherAttributes = FarmOtherAttributesSerializer(roles, many=True).data
    return {"id": farm_id, "farmName": farm_name, "farmOtherAttributes": farmOtherAttributes}


@api_view(['POST'])
def query_page(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    if not page_params_verify(request) is None:
        return page_params_verify(request)

    data = json.loads(request.body)

    # 分页查询农场列表
    query_farm_sql = "select * from user_info where deleted = '0' "
    if "farmName" in data:
        query_farm_sql += " and `farm_name` like '%%{0}%%' "
        query_farm_sql = query_farm_sql.format(data["farmName"])
    roles = UserInfo.objects.raw(query_farm_sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = UserInfoSerializer(page_roles, many=True)

    result = []
    for user in roles_ser.data:
        result.append(getFarmOtherAttributes(user["id"], user["farmName"], data))
    return ok_page(request, roles.__len__(), result)


@api_view(['POST'])
def query_info(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")

    data = json.loads(request.body)
    if "dataTime" not in data:
        return error("dataTime 不能為空")
    if "farmId" not in data:
        return error("farmId 不能為空")
    info = get_mxa_version_data(data["farmId"], data["dataTime"],data)
    if info is not None:
        return ok({"sensitive": info.sensitive, "intermediate": info.intermediate,
                   "resistant": info.resistant, "antibiotic": info.antibiotic, "bacterialType": info.bacterial_type})
    else:
        return ok("")


@api_view(['POST'])
def query_date(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "farmId" not in data:
        return error("farmId 不能為空")
    sql = " SELECT * FROM farm_other_attributes_info  WHERE  farm_id = '%s' " % data["farmId"];
    if "antibiotic" in data:
        sql += " and antibiotic = '%s' " % data["farmId"];
    if "bacterialType" in data:
        sql += " and bacterial_type = '%s' " % data["bacterialType"];
    sql += " GROUP BY data_time ORDER BY data_time DESC"
    if settings.DEBUG:
        print("查询农场其他信息，SQL = '%s' " % sql)
    roles = FarmOtherAttributesInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = FarmOtherAttributesSerializer(page_roles, many=True)
    return ok_all_date(roles_ser.data)


@api_view(['GET'])
def query_all_antibiotic(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    sql = "select * from farm_other_attributes_info "
    roles = FarmOtherAttributesInfo.objects.raw(sql)
    roles_ser = FarmOtherAttributesSerializer(roles, many=True)
    returnData = set()
    for item in roles_ser.data:
        if (item["antibiotic"] is not None and item["antibiotic"] != ""):
            returnData.add(item["antibiotic"])
    return ok(returnData)


@api_view(['GET'])
def query_all_bacterialType(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    sql = "select * from farm_other_attributes_info "
    roles = FarmOtherAttributesInfo.objects.raw(sql)
    roles_ser = FarmOtherAttributesSerializer(roles, many=True)
    returnData = set()
    for item in roles_ser.data:
        if (item["bacterialType"] is not None and item["bacterialType"] != ""):
            returnData.add(item["bacterialType"])
    return ok(returnData)
