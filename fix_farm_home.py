#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vmc_backend.settings')
django.setup()

from farm_home.models import FarmHomeInfo
from django.db import connection

# 需要修复的主键IDs
problematic_ids = [
    '1aa2bd8f13d84c379b83efda59023394',
    'c4a142f77ad14b648fecb37419d578e8'
]

print("开始修复farm_home_info表中的主键冲突...")

# 检查每个ID并尝试修复
for pid in problematic_ids:
    records = FarmHomeInfo.objects.filter(id=pid)
    count = records.count()
    
    if count > 0:
        print(f"找到ID为 {pid} 的记录 {count} 条，删除中...")
        
        # 为确保安全，使用原始SQL删除记录
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM farm_home_info WHERE id = '{pid}'")
            print(f"已从数据库中删除ID为 {pid} 的记录")
    else:
        print(f"未找到ID为 {pid} 的记录，无需修复")

print("修复完成！")

# 在prod环境中还应修复farm_home/views.py中的add方法，
# 应使用get_uuid_str()生成新ID，而不是重用现有ID
print("注意：为了永久解决此问题，建议修改farm_home/views.py中的add方法，确保每次都生成新的UUID") 