# -*- coding: UTF-8 -*-
'''
Created on 2015-12-21

@author: ward
'''
import json
import urllib
from django.http import HttpResponse,JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from basic.basic_response import BasicResponse

def jsonp_wrapped_response(params, data_res, encoder=DjangoJSONEncoder):
    json_obj = None
    if type(data_res) == BasicResponse:
        json_obj = data_res.get_res()
    else:
        json_obj = data_res
    
    jsonp_callback = getattr(settings, 'JSONP_CALLBACK', None)
    if jsonp_callback and params.has_key(jsonp_callback):
        data = '%s(%s)' %(urllib.quote_plus(params[jsonp_callback]), json.dumps(json_obj, cls=encoder))
        return HttpResponse(content=data)
    else:
        return JsonResponse(json_obj, safe=False)
    