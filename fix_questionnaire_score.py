#!/usr/bin/env python
import os
import django
import logging
import sys
from django.db import connections, OperationalError, ProgrammingError

# 设置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("fix_questionnaire_score")

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vmc_backend.settings')
django.setup()

def check_table_exists(table_name):
    """检查表是否存在"""
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            return cursor.fetchone() is not None
    except Exception as e:
        logger.warning(f"检查表 {table_name} 是否存在时出错: {e}")
        return False

def execute_sql(sql, params=None):
    """执行SQL语句"""
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute(sql, params)
            return True
    except Exception as e:
        logger.error(f"执行SQL语句出错: {e}")
        return False

def fix_questionnaire_score_tables():
    """修复问卷评分相关表"""
    # 检查表是否存在
    if check_table_exists('questionnaire_score_info'):
        logger.info("检测到questionnaire_score_info表已存在")
        
        # 确认migration表
        if not check_table_exists('django_migrations'):
            logger.error("django_migrations表不存在，无法修复迁移状态")
            return False
        
        try:
            # 检查问卷评分的迁移是否已应用
            with connections['default'].cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM django_migrations 
                    WHERE app='questionnaire_score' 
                    AND name='0002_questionnairescoreinfo_and_more'
                """)
                migration_exists = cursor.fetchone() is not None
            
            if migration_exists:
                logger.info("迁移 questionnaire_score.0002_questionnairescoreinfo_and_more 已应用")
            else:
                logger.info("迁移 questionnaire_score.0002_questionnairescoreinfo_and_more 未应用，正在添加...")
                
                # 手动添加迁移记录
                successful = execute_sql("""
                    INSERT INTO django_migrations (app, name, applied) 
                    VALUES ('questionnaire_score', '0002_questionnairescoreinfo_and_more', NOW())
                """)
                
                if successful:
                    logger.info("已成功添加迁移记录")
                else:
                    logger.error("添加迁移记录失败")
                    return False
            
            return True
            
        except (OperationalError, ProgrammingError) as e:
            logger.error(f"数据库操作错误: {e}")
            return False
    else:
        logger.info("questionnaire_score_info表不存在，不需要修复")
        return True

def fix_user_info_table():
    """尝试修复user_info表问题"""
    if not check_table_exists('user_info') and check_table_exists('auth_user'):
        logger.info("user_info表不存在但auth_user表存在，尝试手动创建user_info表...")
        
        # 这里需要根据实际的表结构定义正确的CREATE TABLE语句
        # 以下是一个示例，实际应用中需要替换为正确的表结构
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS `user_info` (
          `id` varchar(64) NOT NULL,
          `username` varchar(20) NOT NULL,
          `password` varchar(50) NOT NULL,
          `email` varchar(50) DEFAULT NULL,
          `phone` varchar(20) DEFAULT NULL,
          `farm_name` varchar(50) DEFAULT NULL,
          `sex` char(1) DEFAULT NULL,
          `last_logon_time` varchar(50) DEFAULT NULL,
          `is_admin` char(1) DEFAULT NULL,
          `status` char(1) DEFAULT NULL,
          `create_time` varchar(50) DEFAULT NULL,
          `create_by` varchar(50) DEFAULT NULL,
          `update_time` varchar(50) DEFAULT NULL,
          `update_by` varchar(50) DEFAULT NULL,
          `deleted` char(1) DEFAULT '0',
          PRIMARY KEY (`id`),
          UNIQUE KEY `username` (`username`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        
        if execute_sql(create_table_sql):
            logger.info("已成功创建user_info表")
            
            # 标记迁移为已应用
            if execute_sql("""
                INSERT INTO django_migrations (app, name, applied) 
                VALUES ('user', '0001_initial', NOW())
            """):
                logger.info("已成功添加user迁移记录")
                return True
            else:
                logger.error("添加user迁移记录失败")
                return False
        else:
            logger.error("创建user_info表失败")
            return False
    else:
        logger.info("user_info表已存在或auth_user表不存在，不需要修复")
        return True

if __name__ == "__main__":
    logger.info("开始修复问卷评分和用户相关表...")
    
    # 修复问卷评分表
    if fix_questionnaire_score_tables():
        logger.info("问卷评分表修复成功")
    else:
        logger.error("问卷评分表修复失败")
        sys.exit(1)
    
    # 修复用户表
    if fix_user_info_table():
        logger.info("用户表修复成功")
    else:
        logger.error("用户表修复失败")
        sys.exit(1)
    
    logger.info("所有修复完成")
    sys.exit(0) 