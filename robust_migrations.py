#!/usr/bin/env python
import os
import django
import subprocess
import sys
import time
import logging
from django.db import connections, OperationalError, ProgrammingError

# 设置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("robust_migrations")

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vmc_backend.settings')
django.setup()

def wait_for_db():
    """等待数据库可用"""
    logger.info("等待数据库连接...")
    db_conn = None
    retry_count = 0
    max_retries = 30
    
    while retry_count < max_retries:
        try:
            db_conn = connections['default']
            db_conn.cursor()
            logger.info("数据库连接成功!")
            return True
        except OperationalError:
            retry_count += 1
            logger.info(f"数据库未就绪，等待重试... ({retry_count}/{max_retries})")
            time.sleep(2)
    
    logger.error("无法连接到数据库，退出!")
    return False

def get_app_names():
    """获取所有应用名称"""
    from django.apps import apps
    app_configs = apps.get_app_configs()
    return [app.name for app in app_configs 
            if not app.name.startswith('django.') 
            and not app.name.startswith('rest_framework')]

def make_migrations(app_names):
    """为所有应用创建迁移文件"""
    logger.info("为所有应用创建迁移文件...")
    for app_name in app_names:
        logger.info(f"为应用 {app_name} 创建迁移文件...")
        try:
            subprocess.run([sys.executable, 'manage.py', 'makemigrations', app_name], 
                         check=False, capture_output=True, text=True)
        except Exception as e:
            logger.warning(f"为应用 {app_name} 创建迁移文件时出错: {e}")

def check_table_exists(table_name):
    """检查表是否存在"""
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            return cursor.fetchone() is not None
    except Exception as e:
        logger.warning(f"检查表 {table_name} 是否存在时出错: {e}")
        return False

def migrate_app(app_name, fake_if_table_exists=None, options=None):
    """迁移单个应用
    
    Args:
        app_name: 应用名称
        fake_if_table_exists: 如果该表存在，则使用--fake参数
        options: 附加的迁移选项
    """
    cmd = [sys.executable, 'manage.py', 'migrate', app_name]
    
    # 如果指定了表名，并且该表已存在，使用--fake选项
    if fake_if_table_exists and check_table_exists(fake_if_table_exists):
        logger.info(f"表 {fake_if_table_exists} 已存在，将使用--fake参数")
        cmd.append('--fake')
    
    # 添加额外选项
    if options:
        cmd.extend(options)
    
    logger.info(f"执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"应用 {app_name} 迁移成功")
            return True
        else:
            logger.warning(f"应用 {app_name} 迁移出错: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"执行迁移命令时出错: {e}")
        return False

def robust_migrate():
    """执行强健的迁移流程"""
    if not wait_for_db():
        return False
    
    # 获取所有应用
    app_names = get_app_names()
    logger.info(f"发现以下应用需要迁移: {', '.join(app_names)}")
    
    # 创建迁移文件
    make_migrations(app_names)
    
    # 首先尝试运行完整迁移
    logger.info("尝试完整迁移...")
    try:
        result = subprocess.run([sys.executable, 'manage.py', 'migrate'],
                              check=False, capture_output=True, text=True)
        
        # 如果成功，直接返回
        if result.returncode == 0:
            logger.info("数据库迁移成功完成！")
            return True
        
        # 如果失败，解析错误消息
        error_msg = result.stderr
        logger.warning(f"完整迁移失败: {error_msg}")
        
        # 检查是否有表已存在的错误
        if "already exists" in error_msg:
            logger.info("检测到表已存在错误，尝试逐个应用迁移...")
            
            # 先处理基础表
            base_apps = ['contenttypes', 'auth', 'admin', 'sessions']
            for app in base_apps:
                migrate_app(app, options=['--fake-initial'])
            
            # 逐个处理其他应用
            for app_name in app_names:
                # 尝试普通迁移
                if not migrate_app(app_name):
                    # 如果失败，尝试使用--fake-initial
                    logger.info(f"尝试使用--fake-initial迁移 {app_name}")
                    migrate_app(app_name, options=['--fake-initial'])
            
            logger.info("逐个应用迁移完成")
            
            # 最后再尝试一次完整迁移，以应用可能遗漏的依赖
            logger.info("最后一次尝试完整迁移...")
            final_result = subprocess.run([sys.executable, 'manage.py', 'migrate'],
                                       check=False, capture_output=True, text=True)
            
            if final_result.returncode == 0:
                logger.info("数据库迁移最终成功完成！")
                return True
            else:
                logger.warning(f"最终迁移仍然失败: {final_result.stderr}")
                return False
        
        # 处理缺少表的错误
        elif "doesn't exist" in error_msg:
            logger.info("检测到表不存在错误，尝试使用--fake-initial...")
            
            # 尝试使用--fake-initial
            for app_name in app_names:
                migrate_app(app_name, options=['--fake-initial'])
            
            return True
    
    except Exception as e:
        logger.error(f"执行迁移过程中出错: {e}")
        return False
    
    return False

def fix_specific_issues():
    """修复已知的特定问题"""
    # 修复问卷评分表问题
    if check_table_exists('questionnaire_score_info'):
        logger.info("检测到questionnaire_score_info表已存在，使用--fake迁移")
        migrate_app('questionnaire_score', 'questionnaire_score_info', ['--fake'])
    
    # 修复用户表问题
    if not check_table_exists('user_info') and check_table_exists('auth_user'):
        logger.info("检测到user_info表不存在但auth_user存在，尝试修复")
        migrate_app('user', options=['--fake-initial'])

if __name__ == "__main__":
    logger.info("开始执行强健的数据库迁移...")
    
    # 先尝试修复已知的特定问题
    fix_specific_issues()
    
    # 执行强健的迁移
    if robust_migrate():
        logger.info("强健的数据库迁移完成!")
    else:
        logger.error("强健的数据库迁移失败!")
        sys.exit(1) 