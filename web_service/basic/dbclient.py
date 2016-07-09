# -*- coding: UTF-8 -*-
'''
@author: ward
'''
from django.conf import settings
from utils.db.mongoop import MongoClassSimple

reports_client = MongoClassSimple(settings.REPORTS_DB)