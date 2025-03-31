#!/usr/bin/env python
import os
import django
import hashlib
import logging
import sys
from django.db import OperationalError, ProgrammingError

# 设置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("insert_admin")

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vmc_backend.settings')
django.setup()

def check_table_exists(table_name):
    """检查表是否存在"""
    from django.db import connections
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            return cursor.fetchone() is not None
    except Exception as e:
        logger.warning(f"检查表 {table_name} 是否存在时出错: {e}")
        return False

# MD5加密函数，与系统中使用的相同
def md5_encrypt(password):
    return hashlib.new('md5', bytes(password, encoding='utf-8')).hexdigest()

def create_admin_user():
    try:
        from user.models import UserInfo
        from django.db.models import Q
        from common.time_utils import get_format_time

        logger.info(f"密码 '12345678' 的MD5哈希值: {md5_encrypt('12345678')}")

        # 检查用户表是否存在
        if not check_table_exists('user_info'):
            logger.error("user_info表不存在，无法创建管理员用户")
            return False

        # 检查用户是否已存在
        try:
            admin_exists = UserInfo.objects.filter(Q(username='sysadmin')).exists()
            
            if admin_exists:
                logger.info("管理员用户 'sysadmin' 已存在，正在更新密码...")
                UserInfo.objects.filter(Q(username='sysadmin')).update(
                    password=md5_encrypt('12345678')
                )
                logger.info("密码已更新")
            else:
                logger.info("正在创建管理员用户...")
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
                logger.info("管理员用户创建成功")

            logger.info(f"用户名: sysadmin")
            logger.info(f"密码: 12345678")
            logger.info(f"密码MD5值: {md5_encrypt('12345678')}")
            return True
        
        except (OperationalError, ProgrammingError) as e:
            logger.error(f"数据库操作错误: {e}")
            return False
            
    except ImportError as e:
        logger.error(f"导入模块错误: {e}")
        return False
    except Exception as e:
        logger.error(f"创建管理员用户时出错: {e}")
        return False

if __name__ == "__main__":
    logger.info("开始创建/更新管理员用户...")
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        if create_admin_user():
            logger.info("管理员用户处理完成")
            sys.exit(0)
        else:
            retry_count += 1
            if retry_count < max_retries:
                logger.warning(f"创建管理员用户失败，将重试 ({retry_count}/{max_retries})...")
            else:
                logger.error("创建管理员用户失败，已达到最大重试次数")
    
    # 如果重试都失败了，但不想因此阻止应用启动，可以选择正常退出
    # 如果希望在管理员创建失败时阻止应用启动，则取消下面的注释
    # sys.exit(1) 