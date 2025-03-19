# chat/views.py
import json

from django.shortcuts import render
from rest_framework.decorators import api_view

from chat.serializers import MsgInfoSerializer
from chat.models import MsgInfo
from common.custon_page_conf.custom_page import CustomPagePagination
from common.custom_response import ok_page, error, ok
from common.token_utils import is_ordinary_users_login
from common.custom_page_params_verify import page_params_verify
from vmc_backend import settings


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name, token):
    return render(request, "chat/room.html", {"room_name": room_name, "token": token})


@api_view(['POST'])
def query_chat_object(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    if not page_params_verify(request) is None:
        return page_params_verify(request)

    sql = """
    SELECT t1.* FROM chat_msg_info t1
    INNER JOIN (
        SELECT MAX(id) as max_id
        FROM chat_msg_info
        WHERE send_id = %s OR accept_id = %s
        GROUP BY 
            CASE 
                WHEN send_id = %s THEN accept_id
                ELSE send_id
            END
    ) t2 ON t1.id = t2.max_id
    ORDER BY t1.timestamp DESC
    """
    
    roles = MsgInfo.objects.raw(sql, [user_id, user_id, user_id])
    
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = MsgInfoSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)

@api_view(['POST'])
def query_page(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    if not page_params_verify(request) is None:
        return page_params_verify(request)
    data = json.loads(request.body)
    if "sendId" not in data:
        return error("sendId 不能為空")
    if "acceptId" not in data:
        return error("acceptId 不能為空")
    sql = "select * from chat_msg_info where (send_id = '{0}' and accept_id = '{1}') or (send_id = '{2}' and accept_id = '{3}') order by timestamp ".format(
        data["sendId"], data["acceptId"], data["acceptId"], data["sendId"])
    if settings.DEBUG:
        print("查询聊天记录，sql = %s" % sql)
    roles = MsgInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = MsgInfoSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)


@api_view(['POST'])
def query_self_page(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    sql = "select * from chat_msg_info where send_id = '{0}' or accept_id = '{1}' order by timestamp ".format(user_id,
                                                                                                                user_id)
    if settings.DEBUG:
        print("查询本人聊天记录，sql = %s" % sql)
    roles = MsgInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = MsgInfoSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)
