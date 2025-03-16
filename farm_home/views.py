import json

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from chicken_flock.models import ChickenFlockInfo
from chicken_flock.serializers import ChickenFlockSerializer
from common.custom_response import error, ok
from common.custon_page_conf.custom_page import CustomPagePagination
from common.time_utils import get_format_time
from common.token_utils import is_ordinary_users_login
from common.uuid_utils import get_uuid_str
from farm_home.models import FarmHomeInfo
from vmc_backend import settings
from vmc_backend.settings import FARM_DEFAULT_BREEDING_QUOTE


# 每个人只有一条养殖记录，每次修改数据，版本号新增1
# 获取最大版本数据
def get_mxa_version_data(user_id):
    # 查询当前用户最大版本数据
    sql = "SELECT t1.* FROM farm_home_info t1 INNER JOIN ( SELECT t.user_id, MAX( t.data_version ) AS data_version FROM farm_home_info t where t.user_id = '%s' ) t2 ON t1.data_version = t2.data_version  AND t1.user_id = t2.user_id " % user_id
    if settings.DEBUG:
        print("查询养殖记录最大版本数据，执行SQL=[ %s ]" % sql)
    roles = FarmHomeInfo.objects.raw(sql)
    if len(roles) <= 0:
        return None
    return roles[0]


@api_view(['POST'])
def add(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "breedingQuota" not in data:
        return error("breedingQuota 不能為空")
    if "chickenSeedlingsType" not in data:
        return error("chickenSeedlingsType 不能為空")
    if "breedingMethods" not in data:
        return error("breedingMethods 不能為空")
    if "chickenSeedlingsNumber1" not in data:
        return error("chickenSeedlingsNumber1 不能為空")
    if "chickenSeedlingsNumber2" not in data:
        return error("chickenSeedlingsNumber2 不能為空")
    if "chickenSeedlingsNumber3" not in data:
        return error("chickenSeedlingsNumber3 不能為空")
    if "chickenSeedlingsVolume1" not in data:
        return error("chicken_seedlings_volume1 不能為空")
    if "chickenSeedlingsVolume2" not in data:
        return error("chicken_seedlings_volume2 不能為空")
    if "chickenSeedlingsVolume3" not in data:
        return error("chicken_seedlings_volume3 不能為空")
    info = get_mxa_version_data(user_id)
    data_version = '0' if info is None else info.data_version
    uuid = get_uuid_str() if info is None else info.id

    FarmHomeInfo.objects.create(id=uuid, user_id=user_id, breeding_quota=data["breedingQuota"],
                                chicken_seedlings_type=data["chickenSeedlingsType"],
                                breeding_methods=data["breedingMethods"],
                                chicken_seedlings_number1=data["chickenSeedlingsNumber1"],
                                chicken_seedlings_number2=data["chickenSeedlingsNumber2"],
                                chicken_seedlings_number3=data["chickenSeedlingsNumber3"],
                                chicken_seedlings_volume1=data["chickenSeedlingsVolume1"],
                                chicken_seedlings_volume2=data["chickenSeedlingsVolume2"],
                                chicken_seedlings_volume3=data["chickenSeedlingsVolume3"],
                                data_version=int(data_version) + 1,
                                create_time=get_format_time(),
                                create_by=user_id,
                                update_time=get_format_time(),
                                update_by=user_id,
                                deleted='0',
                                )
    return ok("成功")


@api_view(['GET'])
def query_page(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    role = get_mxa_version_data(user_id)
    if role is None:
        item = {"breedingQuota": FARM_DEFAULT_BREEDING_QUOTE, "chickenSeedlingsType": [], "breedingMethods": "",
                "chickenSeedlingsNumber1": "", "chickenSeedlingsNumber2": "",
                "chickenSeedlingsNumber3": "", "chickenSeedlingsVolume1": "", "chickenSeedlingsVolume2": "",
                "chickenSeedlingsVolume3": ""
                }
        return ok(item)
    else:
        # 调整返回前端数据格式
        chicken_seedlings_type = str(role.chicken_seedlings_type).replace("'", "").replace(" ", "")
        chicken_seedlings_type = chicken_seedlings_type[1:len(chicken_seedlings_type) - 1]
        item = {"breedingQuota": role.breeding_quota, "chickenSeedlingsType": chicken_seedlings_type.split(","),
                "breedingMethods": role.breeding_methods,
                "chickenSeedlingsNumber1": role.chicken_seedlings_number1,
                "chickenSeedlingsNumber2": role.chicken_seedlings_number2,
                "chickenSeedlingsNumber3": role.chicken_seedlings_number3,
                "chickenSeedlingsVolume1": role.chicken_seedlings_volume1,
                "chickenSeedlingsVolume2": role.chicken_seedlings_volume2,
                "chickenSeedlingsVolume3": role.chicken_seedlings_volume3
                }
        return ok(item)


@api_view(['GET'])
def query_batch(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")

    # 查询当前用户最大版本数据
    sql = ("SELECT t1.* FROM chicken_flock_info t1 INNER JOIN ( SELECT t.user_id, MAX( t.data_version ) AS "
           "data_version,t.id FROM chicken_flock_info t where 1 = 1  and t.user_id = '%s' and deleted = '0' ") % user_id
    sql += " GROUP BY t.id ) t2 ON t1.data_version = t2.data_version  AND t1.user_id = t2.user_id and t1.id = t2.id"
    roles = ChickenFlockInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = ChickenFlockSerializer(page_roles, many=True)
    return ok(roles_ser.data)
