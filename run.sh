#!/bin/bash

# Wait for MySQL to be ready
echo "Waiting for MySQL..."
while ! nc -z $MYSQL_HOST 3306; do
  sleep 1
done
echo "MySQL is ready!"

# Wait for Redis to be ready
echo "Waiting for Redis..."
while ! nc -z $REDIS_HOST 6379; do
  sleep 1
done
echo "Redis is ready!"

# Run migrations
python manage.py migrate

# Start the application
python manage.py runserver 0.0.0.0:8000
