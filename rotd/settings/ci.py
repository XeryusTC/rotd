# -*- coding: utf-8 -*-
from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.postgresql_psycopg2",
        "NAME":     "wzive_ci",
        "USER":     "postgres",
        "PASSWORD": "",
        "HOST":     "localhost",
        "PORT":     "",
    },
}
