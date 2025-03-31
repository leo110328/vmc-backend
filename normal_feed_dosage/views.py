import json

from django.db.models import Q
from rest_framework.decorators import api_view

from common.custom_page_params_verify import page_params_verify
from common.custom_response import error, ok, ok_page, ok_all_date
from common.custon_page_conf.custom_page import CustomPagePagination
from common.time_utils import get_format_time
from common.token_utils import is_ordinary_users_login, is_admin_users_login
from common.uuid_utils import get_uuid_str
from normal_feed_dosage.models import NormalFeedDosageInfo
from vmc_backend import settings
from .serializers import NormalFeedDosageInfoSerializer


# Create your views here.


# 获取最大版本数据
def get_mxa_version_data(user_id, date_time):
    # 查询当前用户最大版本数据
    sql = " SELECT t1.* FROM normal_feed_dosage_info t1 INNER JOIN ( SELECT t.user_id, t.data_time,MAX( t.data_version ) AS data_version FROM normal_feed_dosage_info t where 1 = 1 and t.user_id = '%s' " % user_id
    if date_time is not None:
        sql += "and data_time = '%s' " % date_time
    sql += " and deleted = '0' GROUP BY data_time  ) t2 ON t1.data_version = t2.data_version  	AND t1.data_time = t2.data_time  AND t1.user_id = t2.user_id"
    if settings.DEBUG:
        print("查询饲料用量数据最大版本数据，执行SQL=[ %s ]" % sql)
    roles = NormalFeedDosageInfo.objects.raw(sql)
    if len(roles) <= 0:
        return None
    return roles[0]


@api_view(['POST'])
def add(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "chickenSeedFineFeedDosage" not in data:
        return error("每月鸡苗精料用量 不能為空")
    if "chickenDevelopFineFeedDosage" not in data:
        return error("每月中鸡精料用量 不能為空")
    if "chickenMatureFineFeedDosage" not in data:
        return error("每月大鸡精料用量 不能為空")
    if "chickenLayingHensFineFeedDosage" not in data:
        return error("每月下单母鸡精料用量 不能為空")
    if "chickenLaterBorrowingFineFeedDosage" not in data:
        return error("每月後借母鸡精料用量 不能為空")
    if "chickenCockFineFeedDosage" not in data:
        return error("每月公鸡精料用量 不能為空")
    if "dataTime" not in data:
        return error("dataTime 不能為空")
    info = get_mxa_version_data(user_id, data["dataTime"])
    data_version = '0' if info is None else info.data_version
    # 修复: 始终生成新的UUID，而不是重用现有ID
    uuid = get_uuid_str()
    NormalFeedDosageInfo.objects.create(id=uuid, user_id=user_id,
                                        chicken_seed_fine_feed_dosage=data["chickenSeedFineFeedDosage"],
                                        chicken_develop_fine_feed_dosage=data["chickenDevelopFineFeedDosage"],
                                        chicken_mature_fine_feed_dosage=data["chickenMatureFineFeedDosage"],
                                        chicken_laying_hens_fine_feed_dosage=data["chickenLayingHensFineFeedDosage"],
                                        chicken_later_borrowing_fine_feed_dosage=data[
                                            "chickenLaterBorrowingFineFeedDosage"],
                                        chicken_cock_fine_feed_dosage=data["chickenCockFineFeedDosage"],
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
    roles = NormalFeedDosageInfo.objects.filter(Q(id=id))
    if len(roles) <= 0:
        return error("数据不存在")
    roles.update(deleted="1")
    return ok("成功")


#
@api_view(['POST'])
def query_page(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    if not page_params_verify(request) is None:
        return page_params_verify(request)

    data = json.loads(request.body)
    sql = " SELECT t1.* FROM normal_feed_dosage_info t1 INNER JOIN ( SELECT t.user_id, t.data_time,MAX( t.data_version ) AS data_version FROM normal_feed_dosage_info t where 1 = 1 and t.user_id = '%s' " % user_id
    if "dataTime" in data:
        sql += "and data_time = '%s' " % data["dataTime"]
    sql += " and deleted = '0' GROUP BY data_time  ) t2 ON t1.data_version = t2.data_version  	AND t1.data_time = t2.data_time  AND t1.user_id = t2.user_id"
    if settings.DEBUG:
        print("查询饲料数据，执行SQL=[ %s ]" % sql)

    roles = NormalFeedDosageInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = NormalFeedDosageInfoSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)


@api_view(['GET'])
def query_date(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    sql = " SELECT * FROM normal_feed_dosage_info  WHERE  user_id = '%s'  GROUP BY DATA_TIME ORDER BY DATA_TIME DESC " % user_id
    roles = NormalFeedDosageInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = NormalFeedDosageInfoSerializer(page_roles, many=True)
    return ok_all_date(roles_ser.data)
