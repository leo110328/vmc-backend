#!/bin/bash

# 如果容器正在运行，则在容器内执行数据库迁移
if [ "$(docker ps -q -f name=vmc-backend)" ]; then
    echo "容器正在运行，在容器内执行数据库迁移..."
    docker exec -it vmc-backend python init_db.py
else
    echo "容器未运行，启动容器..."
    docker-compose up -d
    echo "等待容器启动..."
    sleep 10
    echo "在容器内执行数据库迁移..."
    docker exec -it vmc-backend python init_db.py
fi

echo "迁移完成！" 