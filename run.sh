#bin/base
cd /opt/vmc-backend && source fram/bin/activate && nohup  python manage.py runserver 0.0.0.0:8000 &
