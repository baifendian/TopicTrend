# -*- coding: UTF-8 -*-
'''
Created on 2015-9-16

@author: ward
'''
from functools import wraps
from django.utils.decorators import available_attrs
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

operations = {
     'VIEW': 'view',
     'ADD': 'add',
     'EDIT': 'edit',
     'DELETE': 'delete',
     'ALLOCATION': 'allocation',
}

def _check_perms(user, perm):
    # First check if the user has the permission (even anon users)
    app, operation, module = perm.split('.')
    app_module_perm = app.lower()+'.'+operation.lower()+'_'+module.lower()
    return user.has_perm(app_module_perm)

def _cus_user_passes_test(test_func, redirect_to):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            from django.http import HttpResponseRedirect
#             if perm:
#                 print perm
#                 print redirect_to
#                 redirect_to += u'?perm=%s'%perm 
            return HttpResponseRedirect(redirect_to)
        return _wrapped_view
    return decorator

def cus_perm_required(perm, redirect_to, raise_exception=False):
    """
    customize permission authenticate
    """
    def _dec_check_perms(user):
        return _check_perms(user, perm)
    return _cus_user_passes_test(_dec_check_perms, redirect_to)


def permission_add(module, using=None):
    '''
    添加自定义权限
    '''
    content_type = None
    try:
        if not using:
            content_type = ContentType.objects.get(app_label=settings.PERMISSION_APP, model=module)
        else:
            content_type = ContentType.objects.using(using).get(app_label=settings.PERMISSION_APP, model=module)
    except:
        content_type = ContentType(name=module, app_label=settings.PERMISSION_APP, model=module)
        content_type.save(using=using)
        
    for op in operations.values():
        try:
            perm = Permission(codename='%s_%s'%(op,module),name='can %s %s'%(op,module),content_type=content_type)
            perm.save(using=using)
        except:
            pass

def check_permission(user, appkey, operator):
    if not (user and appkey and operator):
        return False
    return _check_perms(user, '%s.%s.%s'%(settings.PERMISSION_APP, operator, appkey))
