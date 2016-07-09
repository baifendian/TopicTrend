# -*- coding: UTF-8 -*-
'''
Created on 2015-11-23

@author: ward
'''
import types

def decode(chars):
    '''
    '''
    if type(chars) == types.UnicodeType:
        return chars
    
    if type(chars) != types.StringType:
        raise TypeError('not string type')
    
    try:
        chars = chars.decode('utf8')
    except:
        try:
            chars = chars.decode('gbk')
        except:
            pass
    return chars

if __name__ == '__main__':
    # import unittest
    # unittest.TestCase
    # assertRaisesRegexp
    assert  decode(u'无的') == u'无的'
    decode(['无的'])
    
    