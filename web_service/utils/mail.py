# -*- coding: UTF-8 -*-
'''
Created on 2015-8-26

@author: ward
'''

from django.conf import settings
from django.core.mail import EmailMessage

def send_mail(subject, message, emails, content_subtype='html'):
    msg = EmailMessage(subject, 
                       message, 
                       '%s<%s>'%(settings.EMAIL_USERNAME_ZH, \
                                 settings.EMAIL_HOST_USER), \
                       emails)
    msg.content_subtype = content_subtype
    return msg.send(fail_silently=True)

