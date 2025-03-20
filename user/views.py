import json
import random
import re
import string

from django.core.cache import cache
from django.core.cache import caches

from common.custom_page_params_verify import page_params_verify
from common.email_utils import send_email
from common.token_utils import is_admin_users_login, is_ordinary_users_login
from user.serializers import UserInfoSerializer
from rest_framework.decorators import api_view
from django.db.models import Q
from common.aes_utils import md5_encrypt
from common.custom_response import ok, error, ok_page
from common.time_utils import get_format_time
from common.uuid_utils import get_uuid_str, get_default_id
from common.custon_page_conf.custom_page import CustomPagePagination
from user.models import UserInfo
from vmc_backend import system_conf, settings


def validate_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None


def check_login_parameter(request):
    data = json.loads(request.body)
    if "username" not in data:
        return error("username 不能為空")
    if "email" not in data:
        return error("email 不能為空")
    if "phone" not in data:
        return error("phone 不能為空")
    if len(UserInfo.objects.filter(Q(username=data["username"]))) != 0:
        return error("username已存在")
    if len(UserInfo.objects.filter(Q(email=data["email"]))) != 0:
        return error("email已存在")
    if len(UserInfo.objects.filter(Q(phone=data["phone"]))) != 0:
        return error("phone已存在")
    if not validate_email(data["email"]):
        return error("email格式不正確")
    return None


# 生成验证码
def generate_code(n):
    all_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    if system_conf.code_type_digit:
        all_chars = string.digits
    result = ""
    count = 0
    while count < n:
        result += random.choice(all_chars)
        count += 1
    return result


# 用户注册获取验证码
@api_view(['POST'])
def get_code_add(request):
    parameter = check_login_parameter(request)
    if not parameter is None:
        return parameter
    data = json.loads(request.body)
    # 生成验证码，并将验证码保存到redis中，有效期為5分钟
    code = generate_code(4)
    code_key = "code_0_" + md5_encrypt(data["email"]) + md5_encrypt(data["phone"]) + md5_encrypt(data["email"])
    cache.set(code_key, code, 5 * 60)
    send_email(data["email"], system_conf.email_register_send_template_title,
               system_conf.email_send_template_content.format(code))
    return ok("成功")


@api_view(['POST'])
def add(request):
    # 验证注册其他参数 password/farmName/code
    data = json.loads(request.body)
    if "password" not in data:
        return error("password 不能為空")
    if "code" not in data:
        return error("code 不能為空")
    if "code" not in data:
        return error("code 不能為空")
    code_key = "code_0_" + md5_encrypt(data["email"]) + md5_encrypt(data["phone"]) + md5_encrypt(data["email"])
    code = cache.get(code_key)
    print(code)
    print("用户输入的验证码=" + data["code"])
    # if code is None or code != data["code"]:
    #     return error("验证码错误")
    username = data["username"]
    emails = data["email"]
    phone = data["phone"]
    password = data["password"]
    farm_name = data["farmName"]

    if len(UserInfo.objects.filter(Q(username=username))) != 0:
        return error("username已存在")
    if len(UserInfo.objects.filter(Q(email=emails))) != 0:
        return error("email已存在")
    if len(UserInfo.objects.filter(Q(phone=phone))) != 0:
        return error("phone已存在")
    UserInfo.objects.create(id=get_uuid_str(), username=username, password=md5_encrypt(password), email=emails,
                            phone=phone, farm_name=farm_name,
                            sex=0, is_admin=0, status=1, create_time=get_format_time(),
                            create_by="sysadmin",
                            update_time=get_format_time(),
                            update_by="sysadmin",
                            deleted='0', )
    cache.delete(code_key)
    return ok("新增成功")


@api_view(['POST'])
def change_password(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "oldPassword" not in data:
        return error("oldPassword 不能為空")
    if "newPassword" not in data:
        return error("newPassword 不能為空")
    user_info = UserInfo.objects.filter(Q(id=user_id))
    if len(user_info) == 0:
        return error("系统错误")
    if user_info[0].password != md5_encrypt(data["oldPassword"]):
        return error("旧密码错误")
    user_info.update(password=md5_encrypt(data["newPassword"]))
    return ok("成功")


# 重置密码获取验证码
@api_view(['POST'])
def get_code_reset(request):
    data = json.loads(request.body)
    if "username" not in data:
        return error("username 不能為空")
    user_info = UserInfo.objects.filter(Q(username=data["username"]))
    if len(user_info) <= 0:
        # 无法根据用户名查询到用户，有可能被人撞库查询用户名，所以接口返回成功
        return ok("成功")
    # 生成验证码，并将验证码保存到redis中，有效期為5分钟
    code = generate_code(4)
    code_key = "code_1_" + md5_encrypt(data["username"])
    cache.set(code_key, code, 5 * 60)
    send_email(user_info[0].email, system_conf.email_reset_password_send_template_title,
               system_conf.email_send_template_content.format(code))
    return ok("成功")


@api_view(['POST'])
def reset_password(request):
    data = json.loads(request.body)
    if "code" not in data:
        return error("code 不能為空")
    if "username" not in data:
        return error("username 不能為空")
    if "password" not in data:
        return error("password 不能為空")
    code_key = "code_1_" + md5_encrypt(data["username"])
    code = cache.get(code_key)
    if settings.DEBUG:
        print("重置密码,code_key = {}".format(code_key))
        print("重置密码,生成code = {}".format(code))
        print("重置密码,输入code = {}".format(data["code"]))
    if code is None or code != data["code"]:
        return error("验证码错误")
    UserInfo.objects.filter(Q(username=data["username"])).update(password=md5_encrypt(data["password"]))
    cache.delete(code_key)
    return ok("成功")


@api_view(['POST'])
def query_page(request):
    user_id = is_admin_users_login(request)
    if user_id is None:
        return error("沒有許可權")
    if not page_params_verify(request) is None:
        return page_params_verify(request)
    sql = "select * from user_info where deleted = '0' and id !=  '42d83d66fdf0451db16c3fe434f09e61' "
    data = json.loads(request.body)
    if "username" in data:
        sql += " and username like '%%{0}%%'"
        sql = sql.format(data["username"])
    roles = UserInfo.objects.raw(sql)
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = UserInfoSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)


@api_view(['POST'])
def delete(request):
    data = json.loads(request.body)
    if "userId" not in data:
        return error("userId 不能為空")
    UserInfo.objects.filter(id=data["userId"]).delete()
    return ok("成功")


@api_view(['POST'])
def login(request):
    data = json.loads(request.body)
    if "username" not in data:
        return error("username 不能為空")
    if "password" not in data:
        return error("password 不能為空")
    user_info = UserInfo.objects.filter(Q(username=data["username"]) & Q(password=md5_encrypt(data["password"])))
    if len(user_info) == 0:
        return error("用户名或密码错误")
    # 启用单点登录功能
    if system_conf.single_sign_on:
        # 清除当前用户的token,当用户登錄时候，删除当前用户缓存的token
        all_keys = cache.keys('*')
        for key in all_keys:
            if user_info[0].id in cache.get(key):
                cache.delete(key)
    # 缓存token
    token = get_uuid_str()
    cache.set(token, json.dumps(UserInfoSerializer(user_info, many=True).data))
    result = UserInfoSerializer(user_info, many=True).data[0]
    result['token'] = token
    return ok(result)


@api_view(['POST'])
def logout(request):
    user_id = is_admin_users_login(request)
    if user_id is None:
        return error("沒有許可權")
    token = request.META.get('HTTP_TOKEN')
    if token is not None:
        cache.delete(token)
    return ok("成功")
