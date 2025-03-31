import json

from django.db.models import Q
from rest_framework.decorators import api_view

from common.custom_page_params_verify import page_params_verify
from common.custom_response import error, ok, ok_page, ok_all_date
from common.custon_page_conf.custom_page import CustomPagePagination
from common.time_utils import get_format_time
from common.token_utils import is_ordinary_users_login, is_admin_users_login
from common.uuid_utils import get_uuid_str
from feed_warehouse_capacity.models import FeedWarehouseCapacityInfo
from vmc_backend import settings
from .serializers import FeedWarehouseCapacityInfoSerializer


# Create your views here.


# 获取最大版本数据
def get_mxa_version_data(user_id, date_time):
    # 查询当前用户最大版本数据
    sql = " SELECT t1.* FROM feed_warehouse_capacity_info t1 INNER JOIN ( SELECT t.user_id, t.data_time,MAX( t.data_version ) AS data_version FROM feed_warehouse_capacity_info t where 1 = 1 and t.user_id = '%s' " % user_id
    if date_time is not None:
        sql += "and data_time = '%s' " % date_time
    sql += " and deleted = '0' GROUP BY data_time  ) t2 ON t1.data_version = t2.data_version  	AND t1.data_time = t2.data_time  AND t1.user_id = t2.user_id"
    if settings.DEBUG:
        print("查询料盒数据，执行SQL=[ %s ]" % sql)

    roles = FeedWarehouseCapacityInfo.objects.raw(sql)
    if len(roles) <= 0:
        return None
    return roles[0]


@api_view(['POST'])
def add(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "mixedFeedFrequency" not in data:
        return error("mixedFeedFrequency 不能為空")
    if "mixedFeedContainersFrequency" not in data:
        return error("mixedFeedContainersFrequency 不能為空")
    if "chickenSeedMixedFeedContainersFrequency" not in data:
        return error("chickenSeedMixedFeedContainersFrequency 不能為空")
    if "chickenDevelopMixedFeedContainersFrequency" not in data:
        return error("chickenDevelopMixedFeedContainersFrequency 不能為空")
    if "chickenMatureMixedFeedContainersFrequency" not in data:
        return error("chickenMatureMixedFeedContainersFrequency 不能為空")
    if "feedTowerCapacity" not in data:
        return error("feedTowerCapacity 不能為空")
    if "feedTowerNumber" not in data:
        return error("feedTowerNumber 不能為空")
    if "mixedFeedClearNumber" not in data:
        return error("mixedFeedClearNumber 不能為空")
    if "feedTowerClearNumber" not in data:
        return error("feedTowerClearNumber 不能為空")
    if "dataTime" not in data:
        return error("dataTime 不能為空")
    info = get_mxa_version_data(user_id, data["dataTime"])
    data_version = '0' if info is None else info.data_version
    # 修复: 始终生成新的UUID，而不是重用现有ID
    uuid = get_uuid_str()
    FeedWarehouseCapacityInfo.objects.create(id=uuid, user_id=user_id,
                                             mixed_feed_frequency=data["mixedFeedFrequency"],
                                             mixed_feed_containers_frequency=data["mixedFeedContainersFrequency"],
                                             chicken_seed_mixed_feed_containers_frequency=data[
                                                 "chickenSeedMixedFeedContainersFrequency"],
                                             chicken_develop_mixed_feed_containers_frequency=data[
                                                 "chickenDevelopMixedFeedContainersFrequency"],
                                             chicken_mature_mixed_feed_containers_frequency=data[
                                                 "chickenMatureMixedFeedContainersFrequency"],
                                             feed_tower_capacity=data["feedTowerCapacity"],
                                             feed_tower_number=data["feedTowerNumber"],
                                             mixed_feed_clear_number=data["mixedFeedClearNumber"],
                                             feed_tower_clear_number=data["feedTowerClearNumber"],
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
    roles = FeedWarehouseCapacityInfo.objects.filter(Q(id=id))
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
    sql = " SELECT t1.* FROM feed_warehouse_capacity_info t1 INNER JOIN ( SELECT t.user_id, t.data_time,MAX( t.data_version ) AS data_version FROM feed_warehouse_capacity_info t where 1 = 1 and t.user_id = '%s' " % user_id
    if "dataTime" in data:
        sql += "and data_time = '%s' " % data["dataTime"]
    sql += " and deleted = '0' GROUP BY data_time  ) t2 ON t1.data_version = t2.data_version  	AND t1.data_time = t2.data_time  AND t1.user_id = t2.user_id"
    if settings.DEBUG:
        print("查询料盒数据，执行SQL=[ %s ]" % sql)

    roles = FeedWarehouseCapacityInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = FeedWarehouseCapacityInfoSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)


@api_view(['GET'])
def query_date(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    sql = " SELECT * FROM feed_warehouse_capacity_info  WHERE  user_id = '%s'  GROUP BY DATA_TIME ORDER BY DATA_TIME DESC " % user_id
    roles = FeedWarehouseCapacityInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = FeedWarehouseCapacityInfoSerializer(page_roles, many=True)
    return ok_all_date(roles_ser.data)
