#!/usr/bin/env python
import os
import django
import subprocess
import sys

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vmc_backend.settings')
django.setup()

print("开始初始化数据库...")

# 获取所有应用
from django.apps import apps
app_configs = apps.get_app_configs()
app_names = [app.name for app in app_configs if not app.name.startswith('django.') and not app.name.startswith('rest_framework')]

print(f"发现以下应用需要迁移: {', '.join(app_names)}")

# 为每个应用创建迁移文件
for app_name in app_names:
    print(f"为应用 {app_name} 创建迁移文件...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'makemigrations', app_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"为应用 {app_name} 创建迁移文件时出错: {e}")

# 应用所有迁移
print("应用所有迁移...")
try:
    subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
    print("数据库迁移成功完成！")
except subprocess.CalledProcessError as e:
    print(f"应用迁移时出错: {e}") 