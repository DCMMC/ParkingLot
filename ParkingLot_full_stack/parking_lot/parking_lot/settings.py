"""
Django settings for parking_lot project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
# import subprocess

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yz-e%31oh49iux(ye9(d=739rtw#(m3$+h68i$96pzv)c5&s*!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# TODO: 要不要因为安全改成局域网特定几个 ip
ALLOWED_HOSTS = ["*"]

# docker-compose 指定环境变量:
# HOST_ROLE 分 'core'(核心服务器), 'outdoor_camera' 和 'indoor_camera'(车牌识别服务器)
host_role = os.getenv('HOST_ROLE') or 'core'
# 从 '1' 开始, e.g. 如果是二号入口就是 '2'
host_num = os.getenv('HOST_NUM') or '1'
# mongodb 和 redis 的主机名(docker-compose 的)/ip地址
db_host = os.getenv('DB_HOST') or 'db'
redis_host = os.getenv('REDIS_HOST') or 'redis'
# 如果是 localhost, 因为是跑在 docker 的容器使用的
# 虚拟网卡, 所以不能用 localhost
# 只在 Linux 环境测试过
if db_host == 'localhost':
    # -1 用来移除后面奇怪的 '\n' newline char
    db_host = os.popen(
        "echo $(ip route show | awk '/default/ {print $3}')").read()[:-1]
if redis_host == 'localhost':
    redis_host = os.popen(
        "echo $(ip route show | awk '/default/ {print $3}')").read()[:-1]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mongoengine',
    'parking_lot',
    'channels',
    # 停车场信息实时 websocket 更新
    'parking_lot_realtime',
    # 实时车牌识别
    'HyperLPR',
    # 把数据库作为一个单独的 instance app, 这样方便到时候
    # 部署到树莓派上(因为树莓派不需要运行 http server)
    'db_pool',
    'corsheaders',
]

# 该 routing 只用于核心服务器
if host_role == 'core':
    ASGI_APPLICATION = "parking_lot.routing.application"  # 上面新建的 asgi 应用
else:
    ASGI_APPLICATION = 'parking_lot.routing_cameras.application'

CHANNEL_LAYERS = {
    'default': {
        # 这里用到了 channels_redis
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            # 'hosts': [('127.0.0.1', 6379)],
            # docker-compose
            # 'hosts': [('redis', 6379)],
            # !!! `xwt97294597` is only a test password !!!
            "hosts": ["redis://:xwt97294597@" + redis_host + ":6379/0"],
            "symmetric_encryption_keys": [SECRET_KEY],
        },
    }
}

MONGODB_DATABASES = {
    "default": {
        "name": "db",
        # "host": '127.0.0.1',
        "host": db_host,
        "tz_aware": True,  # 设置时区
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}

from mongoengine import connect # noqa

# connect('db', host='127.0.0.1')
# 如果 docker-compose network 不是 host 模式的话
# 到时候 host 可能要改成核心服务器的 ip
# !!! This is only a test password !!!
# db 的名称原来叫 admin...
connect('admin', host=db_host, port=27017,
        username='mongoadmin', password='xwt97294597')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# DCMMC: urls 路由表, 该路由只用于核心服务器
# 摄像头车牌识别外围服务器请使用 urls_cameras.py
# 并且外围服务器并不需要 http/ws server
if host_role == 'core':
    ROOT_URLCONF = 'parking_lot.urls'
else:
    ROOT_URLCONF = 'parking_lot.urls_cameras'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'db_frontend', 'dist'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'parking_lot.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Add for vuejs
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "db_frontend", "dist", "static")
]

# -- dynamic content is saved to here --
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
# 用来存放停车场 json 模型数据
MODELS_ROOT = os.path.join(BASE_DIR, 'models')
MODELS_URL = 'models'

NOT_FOUND_ROOT = os.path.join(BASE_DIR, '404')

CORS_ORIGIN_ALLOW_ALL = True

LOGIN_URL = '/login/index.html'
LOGIN_ROOT = os.path.join(BASE_DIR, 'login')
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# CELERY STUFF
# 到时候要改成核心服务器的 ip
CELERY_BROKER_URL = 'redis://:xwt97294597@' + redis_host + ':6379/0'
CELERY_RESULT_BACKEND = 'redis://:xwt97294597@' + redis_host + ':6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'

# !!! DCMMC: 只是为了调试方便
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
from corsheaders.defaults import default_headers # noqa

CORS_ALLOW_HEADERS = default_headers + (
    'x-token',
)
