#!/usr/bin/env python
import os
import sys
import re
import glob

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 要检查的应用目录
APP_DIRS = [
    'farm_home', 'immunization', 'clear', 'chicken_flock', 'dict_info', 
    'farm_other_attributes', 'feed_warehouse_capacity', 'fine_feed_dosage',
    'medication_use', 'normal_feed_dosage', 'obituary', 'questionnaire_score',
    'notice', 'commodity', 'order', 'shopp_cart'
]

# 用于匹配重用UUID的正则表达式
UUID_REUSE_PATTERN = r'uuid\s*=\s*get_uuid_str\(\)\s+if\s+.*?\s+else\s+.*?\.id'

# 要修复的模式
FIX_FROM = 'uuid = get_uuid_str() if info is None else info.id'
FIX_TO = '''# 修复: 始终生成新的UUID，而不是重用现有ID
    uuid = get_uuid_str()'''

def check_and_fix_file(file_path):
    """检查并修复文件中的UUID重用问题"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否存在UUID重用问题
    if re.search(UUID_REUSE_PATTERN, content):
        print(f"在文件 {file_path} 中发现UUID重用问题")
        
        # 修复问题
        fixed_content = content.replace(FIX_FROM, FIX_TO)
        
        # 保存修复后的文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"已修复文件 {file_path}")
        return True
    
    return False

def main():
    """检查并修复所有应用视图中的UUID重用问题"""
    total_fixed = 0
    
    print("开始检查并修复UUID重用问题...")
    
    for app_dir in APP_DIRS:
        app_path = os.path.join(BASE_DIR, app_dir)
        if not os.path.exists(app_path):
            print(f"应用目录 {app_path} 不存在，跳过")
            continue
        
        views_path = os.path.join(app_path, 'views.py')
        if os.path.exists(views_path):
            if check_and_fix_file(views_path):
                total_fixed += 1
    
    print(f"检查完成，共修复了 {total_fixed} 个文件")
    
    if total_fixed > 0:
        print("\n建议执行以下命令部署修复:")
        print("1. 重启容器: docker-compose down && docker-compose up -d")
        print("2. 或者在容器内更新代码: docker exec -it vmc-backend bash -c 'cd /opt/vmc-backend && git pull'")

if __name__ == "__main__":
    main() 