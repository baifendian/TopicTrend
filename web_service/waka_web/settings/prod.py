# -*- coding: utf-8 -*-
from .common import *

ALLOWED_HOSTS = [
    '.baifendian.com',  # Allow domain and subdomains
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
     },
}

MONGO_ADDR = ['172.24.3.55:27017', ]
REPORTS_DB = 'crawldata'

