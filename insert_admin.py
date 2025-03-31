#!/usr/bin/env python
import os
import django
import hashlib

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vmc_backend.settings')
django.setup()

from user.models import UserInfo
from django.db.models import Q
from common.time_utils import get_format_time

# MD5加密函数，与系统中使用的相同
def md5_encrypt(password):
    return hashlib.new('md5', bytes(password, encoding='utf-8')).hexdigest()

print(f"密码 '12345678' 的MD5哈希值: {md5_encrypt('12345678')}")

# 检查用户是否已存在
admin_exists = UserInfo.objects.filter(Q(username='sysadmin')).exists()

if admin_exists:
    print("管理员用户 'sysadmin' 已存在，正在更新密码...")
    UserInfo.objects.filter(Q(username='sysadmin')).update(
        password=md5_encrypt('12345678')
    )
    print("密码已更新")
else:
    print("正在创建管理员用户...")
    # 创建新管理员用户
    UserInfo.objects.create(
        id='42d83d66fdf0451db16c3fe434f09e61',
        username='sysadmin',
        password=md5_encrypt('12345678'),  # 使用MD5加密的密码
        email='1752476831@qq.com',
        phone='+825223436781',
        farm_name='Lau',
        sex='0',
        last_logon_time='',
        is_admin='1',
        status='1',
        create_time=get_format_time(),
        create_by='sysadmin',
        update_time=get_format_time(),
        update_by='sysadmin',
        deleted='0'
    )
    print("管理员用户创建成功")

print(f"用户名: sysadmin")
print(f"密码: 12345678")
print(f"密码MD5值: {md5_encrypt('12345678')}") 