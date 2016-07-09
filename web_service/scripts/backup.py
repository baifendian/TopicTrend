# -*- coding: UTF-8 -*-
'''
Created on 2015-12-3

@author: ward
'''
import os
import sys 
import time
import django

__version__ = '1.0.1'

'''
备份配置数据
'''

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

env_file = open(os.path.join(BASE_DIR, 'ENV')).readline().strip()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bdi_web_management.settings.%s"%env_file)
django.setup()

from bson.json_util import dumps

from django.conf import settings
from utils.db.mongoop import MongoClassSimple

if __name__ == "__main__":
    backup_dir = os.path.join(os.path.dirname(BASE_DIR), 'bdi_config_backup')
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)
    backup_current = os.path.join(backup_dir, 'backup-%s' %time.strftime('%Y-%m-%d'))
    if not os.path.exists(backup_current):
        os.mkdir(backup_current)
        
    output_file = open(os.path.join(backup_current, 'configInfo'), 'w')
    db_client = MongoClassSimple(settings.CONFIG_DB)
    docs = db_client.find_docs('configInfo', {})
    for line in docs:
        output_file.write(dumps(line))
        output_file.write('\n')
    output_file.close()
    
    print 'exit'
        


