import json

from chicken_flock.models import ChickenFlockInfo, ChickenFlockToInfo
from common.token_utils import is_admin_users_login, is_ordinary_users_login
from rest_framework.decorators import api_view
from django.db.models import Q
from common.custom_response import ok, error, ok_page, get_total_page
from common.time_utils import get_format_time
from common.uuid_utils import get_uuid_str, get_default_id
from user.models import UserInfo
from user.serializers import UserInfoSerializer
from vmc_backend.settings import DEBUG
from .serializers import ChickenFlockSerializer, ChickenFlockToSerializer
from common.custon_page_conf.custom_page import CustomPagePagination


# 获取最大版本数据
def get_mxa_version_data(user_id, uuid):
    # 查询当前用户最大版本数据
    sql = "SELECT t1.* FROM chicken_flock_info t1 INNER JOIN ( SELECT t.user_id, MAX( t.data_version ) AS data_version,t.id FROM chicken_flock_info t where 1 = 1  and t.user_id = '%s' and deleted = '0' " % user_id
    if uuid is not None:
        sql += " and  t.id = '%s' " % uuid
    sql += " GROUP BY t.id ) t2 ON t1.data_version = t2.data_version  AND t1.user_id = t2.user_id and t1.id = t2.id"
    roles = ChickenFlockInfo.objects.raw(sql)
    if len(roles) <= 0:
        return None
    return roles[0]


@api_view(['POST'])
def add(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "batchName" not in data:
        return error("batchName 不能為空")
    ChickenFlockInfo.objects.create(id=get_uuid_str(), user_id=user_id, batch_name=data["batchName"],
                                    status='1',
                                    incubation_date="",
                                    chicken_seedling_number="",
                                    vaccine_manufacturers="",
                                    vaccine_id="",
                                    data_version='1',
                                    create_time=get_format_time(),
                                    create_by=user_id,
                                    update_time=get_format_time(),
                                    update_by=user_id,
                                    deleted='0',
                                    )
    return ok("成功")


@api_view(['POST'])
def update(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "id" not in data:
        return error("id 不能為空")
    if "batchName" not in data:
        return error("batchName 不能為空")
    if "incubationDate" not in data:
        return error("incubationDate 不能為空")
    if "chickenSeedlingNumber" not in data:
        return error("chickenSeedlingNumber 不能為空")
    if "vaccineId" not in data:
        return error("vaccineId 不能為空")
    if "vaccineManufacturers" not in data:
        return error("vaccineManufacturers 不能為空")
    info = get_mxa_version_data(user_id, data["id"])
    if info is None:
        return error("数据不存在")
    if info.status == '0':
        return error("鸡群已关闭,无法编辑")
    data_version = '0' if info is None else info.data_version
    # 修复: 始终生成新的UUID，而不是重用现有ID
    uuid = get_uuid_str()
    ChickenFlockInfo.objects.create(id=uuid, user_id=user_id, batch_name=data["batchName"],
                                    incubation_date=data["incubationDate"],
                                    chicken_seedling_number=data["chickenSeedlingNumber"],
                                    vaccine_id=data["vaccineId"],
                                    vaccine_manufacturers=data["vaccineManufacturers"],
                                    data_version=int(data_version) + 1,
                                    status='1',
                                    create_time=get_format_time(),
                                    create_by=user_id,
                                    update_time=get_format_time(),
                                    update_by=user_id,
                                    deleted='0',
                                    )
    return ok("成功")


@api_view(['POST'])
def query_page(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)

    sql = "SELECT t1.* FROM chicken_flock_info t1 INNER JOIN ( SELECT t.user_id, MAX( t.data_version ) AS data_version,t.id FROM chicken_flock_info t where 1 = 1  and t.user_id = '%s' and deleted = '0' " % user_id
    if "id" in data:
        sql += " and  t.id = '%s' " % id
    if "status" in data:
        sql += " and t.status = '%s'" % data["status"]
    sql += " GROUP BY t.id ) t2 ON t1.data_version = t2.data_version  AND t1.user_id = t2.user_id and t1.id = t2.id"

    roles = ChickenFlockInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = ChickenFlockSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)


@api_view(['GET'])
def close(request, id):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    role = get_mxa_version_data(user_id, id)
    if role is None:
        return error("数据不存在")
    ChickenFlockInfo.objects.filter(id=id).update(status='0')
    return ok("操作成功")


@api_view(['GET'])
def query(request, id):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    role = get_mxa_version_data(user_id, id)
    if role is None:
        return error("数据不存在")
    return ok({"id": id, "batchName": role.batch_name, "incubationDate": role.incubation_date,
               "chickenSeedlingNumber": role.chicken_seedling_number, "vaccineId": role.vaccine_id,
               "vaccineManufacturers": role.vaccine_manufacturers, "status": "已关闭" if role.status == "0" else "活动中"
               })


@api_view(['POST'])
def add_other_attributes(request):
    user_id = is_admin_users_login(request)
    if user_id is None:
        return error("沒有許可權")
    data = json.loads(request.body)
    if "id" not in data:
        return error("id 不能為空")
    if "d1" not in data:
        return error("d1 不能為空")
    if "d2" not in data:
        return error("d2 不能為空")
    if "d3" not in data:
        return error("d3 不能為空")
    info = ChickenFlockInfo.objects.filter(id=data["id"])
    if len(info) <= 0:
        return error("数据不存在")
    else:
        info.update(d1=data["d1"], d2=data["d2"], d3=data["d3"],
                    update_time=get_format_time(),
                    update_by=user_id)
        return ok("成功")


# @api_view(['POST'])
# def query_all(request):
#     user_id = is_ordinary_users_login(request)
#     if user_id is None:
#         return error("未登錄")
#     sql = "SELECT t1.* FROM chicken_flock_info t1 INNER JOIN ( SELECT t.user_id, MAX( t.data_version ) AS data_version,t.id FROM chicken_flock_info t where 1 = 1  and t.user_id = '%s' and deleted = '0' " % user_id
#     sql += " GROUP BY t.id ) t2 ON t1.data_version = t2.data_version  AND t1.user_id = t2.user_id and t1.id = t2.id"
#     roles = ChickenFlockInfo.objects.raw(sql)
#     page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
#     roles_ser = ChickenFlockSerializer(page_roles, many=True)
#     return ok(roles_ser.data)


@api_view(['POST'])
def query_all(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("沒有許可權")

    # 查询所有农场
    data = json.loads(request.body)
    # query_farm_sql = "select * from user_info where deleted = '0'  "
    # if "farmId" in data:
    #     query_farm_sql += " AND id = '%s'" % data['farmId']
    # if "farmName" in data:
    #     query_farm_sql += " AND farm_name = '%s'" % data['farmId']
    # roles = UserInfo.objects.raw(query_farm_sql)
    # if len(roles) <= 0:
    #     return ok([])

    sql = " SELECT 	a.*,b.farm_name from ( SELECT t1.*  FROM chicken_flock_info t1 INNER JOIN ( SELECT t.user_id, MAX( t.data_version ) AS data_version, t.id FROM chicken_flock_info t  WHERE 1 = 1 AND deleted = '0' "
    if "farmId" in data:
        sql += " AND user_id = '%s' " % data['farmId']
    if "chickenId" in data:
        sql += " AND id = '%s' " % data['chickenId']
    sql += " GROUP BY t.id  ) t2 ON t1.data_version = t2.data_version  AND t1.user_id = t2.user_id  AND t1.id = t2.id 	) a INNER JOIN user_info b ON a.user_id = b.id WHERE 1 = 1 "
    if "farmName" in data:
        sql += " AND b.farm_name = '%s'" % data['farmName']
    if DEBUG:
        print("所有农场所有鸡群其他信息，执行sql = %s" % sql)
    roles = ChickenFlockToInfo.objects.raw(sql)
    # page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)

    roles_ser = ChickenFlockToSerializer(roles, many=True)
    return ok({"total": roles.__len__(), "list": roles_ser.data})

    # 查询所有农场的鸡群的其他属性
    # for user in UserInfoSerializer(roles, many=True).data:
    #     sql = "SELECT t1.* FROM chicken_flock_info t1 INNER JOIN ( SELECT t.user_id, MAX( t.data_version ) AS data_version,t.id FROM chicken_flock_info t where 1 = 1  and t.user_id = '%s' and deleted = '0' " % \
    #           user["id"]
    #     if "chickenId" in data:
    #         sql += " and id = '%s' " % data['chickenId']
    #     if "farmId" in data:
    #         sql += " and user_id = '%s' " % data['farmId']
    #     sql += " GROUP BY t.id ) t2 ON t1.data_version = t2.data_version  AND t1.user_id = t2.user_id and t1.id = t2.id"
    #     roles = ChickenFlockInfo.objects.raw(sql)
    #     page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    #     roles_ser = ChickenFlockSerializer(page_roles, many=True)
    #
    #     page = request.query_params["page"]
    #     size = request.query_params["size"]
    #     if int(size) > CustomPagePagination().max_page_size:
    #         size = CustomPagePagination().max_page_size
    #     chicken_flock_info_page = {"page": page, "size": size, "totalNumber": page_roles.__len__(),
    #                                "totalPage": get_total_page(int(page_roles.__len__()), int(size))}
    #
    #     result.append({"id": user["id"], "farmName": user["farmName"],
    #                    "chickenInfo": {"page": chicken_flock_info_page, "list": roles_ser.data}})
    # return ok(result)
