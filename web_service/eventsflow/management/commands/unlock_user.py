# -*- coding: UTF-8 -*-
'''
Created on 2015-11-10

@author: ward
'''
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        print u'===================解锁用户==================='
        while True:
            username = raw_input('请输入用户名(至少5位字符)：')
            if len(username.decode('utf8')) > 4:
                break
            else:
                self.stdout.write(u'============输入的用户名无效，请重新输入============')
        
        from django.core.cache import cache
        from django.conf import settings
        
        login_limit_key = u'%s_%s' %(settings.CACHE_LOGIN_PREFIX, username)
        limit_status = cache.get(login_limit_key)
        if limit_status:
            cache.delete(login_limit_key)
            print 'success.'
        
        print 'exit.'
