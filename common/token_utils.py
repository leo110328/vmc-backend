import json

from django.core.cache import cache
from django.db.models import Q

from common.custom_response import error
from user.models import UserInfo


def get_user_info(request):
    token = request.META.get('HTTP_TOKEN')
    if token is None:
        return None
    use_info = cache.get(token)
    if use_info is None:
        return None
    if len(json.loads(use_info)) <= 0:
        return None
    # token续签
    cache.set(token, use_info)
    return json.loads(use_info)[0]


# 判断当前是否登錄，未登錄，返回None，登錄，返回user_id
def is_ordinary_users_login(request):
    user_info = get_user_info(request)
    if user_info is None:
        return None
    return user_info["id"]


# 判断当前是否登錄，未登錄，返回None，登錄，返回user_id
def is_admin_users_login(request):
    user_info = get_user_info(request)
    if user_info is None:
        return None
    user_info = UserInfo.objects.filter(Q(id=user_info["id"]))
    if len(user_info) <= 0:
        return None
    if user_info[0].is_admin == "1":
        return user_info[0].id
    return None
