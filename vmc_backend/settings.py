"""
Django settings for demo project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import common.custom_render.customrenderer
import common.custom_render.customrenderer
from pathlib import Path

from django.core.management import templates

from vmc_backend import system_conf

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-d4=%iwh*y-4(we-b=2%)t&x4+dnk7(e3y$vmh8-o!8!5%i5x69"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition


INSTALLED_APPS = [
    'resources',
    'common',
    'daphne',
    'chat',
    'user',
    'commodity',
    'order',
    'shopp_cart',
    'notice',
    'immunization',
    'clear',
    'farm_home',
    'farm_other_attributes',
    # 饲料仓库管理
    'feed_warehouse_capacity',
    # 精细饲料用量
    'fine_feed_dosage',
    # 普通饲料用量
    'normal_feed_dosage',
    # 鸡群信息
    'chicken_flock',
    # 死淘率
    'obituary',
    # 用药记录
    'medication_use',
    # 问卷得分
    'questionnaire_score',
    # 字典
    'dict_info',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "common.custom_exception.custom_exception_handler"
]

ROOT_URLCONF = "vmc_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "demo.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
    'default': {
        # 表示使用的是mysql数据库的引擎
        'ENGINE': 'django.db.backends.mysql',
        # 数据库的名字，可以在mysql的提示符下先创建好
        'NAME': '{}'.format(system_conf.mysql_conf_dbname),
        # 数据库用户名
        'USER': '{}'.format(system_conf.mysql_conf_username),
        # 数据库密码
        'PASSWORD': '{}'.format(system_conf.mysql_conf_password),
        # 数据库主机，留空默认為"localhost"
        'HOST': '{}'.format(system_conf.mysql_conf_localhost),
        # 数据库使用的端口
        'PORT': '{}'.format(system_conf.mysql_conf_port),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# MEDIA_ROOT指定了文件上传后的存储路径
MEDIA_ROOT = os.path.join(BASE_DIR, '{}'.format(system_conf.file_root))

# 默认养殖额度
FARM_DEFAULT_BREEDING_QUOTE = 1000

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# mysite/settings.py
# Daphne
ASGI_APPLICATION = "vmc_backend.asgi.application"

# settings.py

# 缓存设置
CACHES = {
    "default": {
        # 使用django-redis的缓存
        "BACKEND": "django_redis.cache.RedisCache",
        # redis数据库的位置
        "LOCATION": "redis://{}:{}/{}".format(system_conf.redis_conf_localhost, system_conf.redis_conf_port,
                                              system_conf.redis_conf_dbname),
        # 缓存超时事件,单位:秒
        'TIMEOUT': "{}".format(system_conf.redis_conf_cache_time),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 1000},
            "DECODE_RESPONSES": True,
            "PASSWORD": "{}".format(system_conf.redis_conf_password),
        }
    }
}

# 聊天缓存设置
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                "redis://:{}@{}:{}/{}".format(system_conf.redis_conf_password, system_conf.redis_conf_localhost,
                                              system_conf.redis_conf_port, system_conf.redis_conf_dbname)
            ]
        },
    },
}
TOKEN_KEY = 1234
# Email Settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '{}'.format(system_conf.email_host)
EMAIL_PORT = '{}'.format(system_conf.email_port)
EMAIL_HOST_USER = '{}'.format(system_conf.email_host_user)
EMAIL_HOST_PASSWORD = '{}'.format(system_conf.email_host_password)
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False

DOMAIN = os.getenv('DOMAIN')
SITE_NAME = 'VMC Web App'
