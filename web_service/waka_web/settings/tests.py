# -*- coding: utf-8 -*-
from .common import *

EMAIL_HOST = 'mail.baifendian.com'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
STATIC_ROOT = ''
STATICFILES_DIRS = (
    os.path.join(DATA_DIR, 'static').replace('\\','/'),
)

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
         'NAME': 'bma_local',                      # Or path to database file if using sqlite3.
         'USER': 'root',                      # Not used with sqlite3.
         'PASSWORD': '1234',                  # Not used with sqlite3.
         'HOST': '172.24.2.50',                              # Set to empty string for localhost. Not used with sqlite3.
         'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
     },
}

MONGO_ADDR = ['172.24.3.55:27017', ]
REPORTS_DB = 'crawldata'
