#!/bin/bash

echo "VMC Backend - 迁移修复工具"
echo "=========================="
echo

# 1. 首先尝试特定问题修复
echo "正在修复特定问题..."
python fix_questionnaire_score.py
if [ $? -ne 0 ]; then
    echo "特定问题修复失败，尝试继续..."
fi

# 2. 运行强健的迁移脚本
echo "正在执行强健的数据库迁移..."
python robust_migrations.py
if [ $? -ne 0 ]; then
    echo "强健的数据库迁移失败"
    exit 1
fi

# 3. 尝试创建管理员用户
echo "正在创建/更新管理员用户..."
python insert_admin.py
if [ $? -ne 0 ]; then
    echo "警告: 管理员用户创建失败，但将继续执行"
fi

echo "修复完成！"
echo "如果应用仍有问题，可能需要重置数据库:"
echo "  docker-compose down"
echo "  docker volume rm vmc-backend_mysql_data"
echo "  docker-compose up -d" 