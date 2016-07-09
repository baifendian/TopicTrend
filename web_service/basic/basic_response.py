# -*- coding: UTF-8 -*-
'''
@author: ward
'''
import types
import json

__doc__ =  '''
    基础ajax请求返回协议：
    {
        'rc': 0,
        'msg': 'OK',
        'data': {},
    }
    
    rc(response code)存在的值：
    0        成功
    1        成功，但部分需求未满足
    4        常规错误
    5        内部服务异常
    9        请登录
    
'''

RC_CODES = {
    'SUCCESS': 0,
    'HALF_SUCCESS':1,
    'ERROR': 4, 
    'INTERNAL_ERROR': 5, 
    'LOGIN': 9,
}

class DataPackage(object):
    def __init__(self, elements=None, fields=None):
        self._data = {'elements': None}
        if elements:
            self.set_elements(elements)
        
        if fields:
            self.set_fields(fields)
    
    def get_data(self):
        return self._data
    
    def set_elements(self, elements):
        if type(elements) == types.ListType or type(elements) == types.DictType:
            self._data['elements'] = elements
        else:
            raise TypeError('elements must be a List or Dict')
        return self
    
    def set_fields(self, fields):
        if type(fields) == types.DictType and 'elements' not in fields:
            self._data.update(fields)
        else:
            raise TypeError('fields must be a Dict and dont contains elements field')
        return self

class BasicResponse(object):
    def __init__(self, response_code=None, msg=None, data=None):
        self._res = {'rc': response_code, 'msg': msg, 'data': data}
    
    def set_rc(self, response_code):
        if type(response_code) == types.IntType:
            self._res['rc'] = response_code
        else:
            raise TypeError('response_code must be a Integer')
        return self
    
    def set_msg(self, msg):
        _msg = None
        if type(msg) == types.UnicodeType:
            _msg = msg.encode()
        elif type(msg) == types.StringType:
            _msg = msg
        else:
            raise TypeError('msg must be a string')
        self._res['msg'] = _msg
        return self
    
    def set_data(self, data):
        if type(data) == DataPackage:
            self._res['data'] = data.get_data()
        else:
            raise TypeError('data s class must be DataPackage')
        return self
    
    def get_res(self):
        return self._res
    
    def serialize(self):
        if self._res['rc'] is None:
            raise AttributeError('response_code must be set')
        return json.dumps(self._res)
    
if __name__ == '__main__':
    d = DataPackage([1,2,3])
    print type(d)
    
    t = BasicResponse()
    t.set_rc(0)
    print t.serialize()
    
    
    