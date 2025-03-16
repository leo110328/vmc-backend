import json
from datetime import datetime

from rest_framework.decorators import api_view
from django.db.models import Q
from common.custom_page_params_verify import page_params_verify
from common.custom_response import ok, error, ok_page
from common.time_utils import get_format_time, is_valid_date
from common.uuid_utils import get_uuid_str, get_default_id
from notice.models import NoticeInfo
from notice.serializers import NoticeInfoSerializer
from common.custon_page_conf.custom_page import CustomPagePagination
from common.token_utils import is_ordinary_users_login, is_admin_users_login
from resources.models import ResourcesInfo


@api_view(['POST'])
def add(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "text" not in data:
        return error("消息内容不能為空")
    if "title" not in data:
        return error("标题不能為空")
    if "resourcesId" not in data:
        return error("resourcesId 不能為空")
    if "msgTime" not in data:
        return error("msgTime 不能為空")
    if is_valid_date(data["msgTime"]) is False:
        return error("msgTime 格式不正確")
    resources_info = ResourcesInfo.objects.filter(id=data["resourcesId"])
    if len(resources_info) == 0:
        return error("resources 不存在")
    NoticeInfo.objects.create(id=get_uuid_str(), text=data["text"], title=data["title"],
                              resources_id=data["resourcesId"], msg_time=data["msgTime"],
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
    if not page_params_verify(request) is None:
        return page_params_verify(request)
    sql = "SELECT a.*  FROM ( SELECT * FROM notice_info where deleted = '0' ORDER BY create_time DESC LIMIT 9999) AS a  GROUP BY DATE_FORMAT(a.msg_time, '%%Y-%%m') "
    roles = NoticeInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = NoticeInfoSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)


# 查询最新消息
@api_view(['POST'])
def query_latest(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")

    roles = NoticeInfo.objects.filter().order_by('-create_time').first()
    if roles is None:
        return ok({"id": "", "text": "", "title": "", "msgTime": "",
                   "resourcesId": ""})
    return ok({"id": roles.id, "text": roles.text, "title": roles.title, "msgTime": roles.msg_time,
               "resourcesId": roles.resources_id})


@api_view(['POST'])
def query_page_month(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "msgTime" not in data:
        return error("msgTime 不能為空")
    if is_valid_date(data["msgTime"]) is False:
        return error("msgTime 格式不正確")
    sql = "SELECT * FROM notice_info where deleted = '0' and DATE_FORMAT(msg_time, '%%Y-%%m') =  DATE_FORMAT('{0}', '%%Y-%%m') ORDER BY create_time desc "
    sql = sql.format(data["msgTime"])
    roles = NoticeInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = NoticeInfoSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)


# 删除订单
@api_view(['GET'])
def delete(request, id):
    user_id = is_admin_users_login(request)
    if user_id is None:
        return error("沒有許可權")
    notice_info = NoticeInfo.objects.filter(id=id)
    if len(notice_info) == 0:
        return error("消息不存在")
    notice_info.delete()
    return ok("操作成功")
