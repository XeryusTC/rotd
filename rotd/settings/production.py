# -*- coding: utf-8 -*-
from .base import *
from .util import get_env_setting

DEBUG = False
DOMAIN = get_env_setting('ROTD_DOMAIN')
ALLOWED_HOSTS = [
        DOMAIN,
    ]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_env_setting('ROTD_DB_NAME'),
        "USER": get_env_setting('ROTD_DB_USER'),
        "PASSWORD": get_env_setting('ROTD_DB_PASSWORD'),
        "HOST": "localhost",
        "PORT": "",
    },
}

SECRET_KEY = get_env_setting('ROTD_SECRET_KEY')

EMAIL_BACKEND = 'django.core.backends.smtp.EmailBackend'
EMAIL_HOST = get_env_setting('ROTD_EMAIL_HOST')
EMAIL_HOST_PASSWORD = get_env_setting('ROTD_EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = get_env_setting('ROTD_EMAIL_HOST_USER')
EMAIL_PORT = get_env_setting('ROTD_EMAIL_PORT')
EMAIL_USE_TLS = True
