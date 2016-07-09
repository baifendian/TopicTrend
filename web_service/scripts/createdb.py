# -*- coding: UTF-8 -*-
'''
Created on 2015-12-7

@author: ward
'''
import os
import sys
import importlib
import MySQLdb

__doc__ == '''
    如果setting文件配置的mysql账户具有创建DB权限，可以使用此脚本.
'''

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

env_file = open(os.path.join(BASE_DIR, 'ENV')).readline().strip()

settings = importlib.import_module('bdi_web_management.settings.%s'%env_file)

db_conf = settings.DATABASES['default']
db_name = db_conf['NAME']
conn_obj = MySQLdb.connect(host=db_conf['HOST'], port=int(db_conf['PORT']), 
                user=db_conf['USER'], passwd=db_conf['PASSWORD'], 
                charset='utf8')

conn_obj.autocommit(True)
_cursor = conn_obj.cursor()
_cursor.execute('CREATE DATABASE IF NOT EXISTS %s default charset utf8 COLLATE utf8_general_ci'%db_name)
_cursor.close()
conn_obj.close()

print 'exit.'
