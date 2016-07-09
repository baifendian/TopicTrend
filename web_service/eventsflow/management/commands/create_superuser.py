# -*- coding: UTF-8 -*-
'''
Created on 2015-11-10

@author: ward
'''
import getpass
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            username = raw_input('请输入用户名(至少5位字符)：')
            if len(username.decode('utf8')) > 4:
                break
            else:
                self.stdout.write(u'============输入的用户名无效，请重新输入============')
        
        while True:
            pwd = getpass.getpass('请输入密码(至少5位字符)：')
            if len(pwd.decode('utf8')) > 4:
                break
            else:
                self.stdout.write(u'============输入的密码无效，请重新输入============')
        
        import md5
        from django.contrib.auth.models import User
        
        md5_pwd = md5.md5(md5.md5(pwd).hexdigest()).hexdigest()
        try:
            User.objects.create_superuser(username, None, md5_pwd)
            self.stdout.write(u'============管理员%s创建成功============'%username)
        except:
            self.stdout.write(u'============用户名已存在============')
        
        print 'exit.'
