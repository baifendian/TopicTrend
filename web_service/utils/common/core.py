# -*- coding: UTF-8 -*-
'''
Created on 2015-6-25

@author: ward
'''
import json
import types

def num_readability(num):
    if types.StringType == type(num):
        return num
    if num <= 0:
        return '0'
    
    decimals = None
    if types.FloatType == type(num):
        integer = str(int(num))
        decimals = str(num)[len(integer):]
        num = int(num)
    
    ret = []
    while num:
        if num/1000:
            ret.insert(0,('000%s'%(num%1000))[-3:])
        else:
            ret.insert(0,'%s'%(num%1000))
        num = num/1000
    
    ret_str = ','.join(ret)
    if decimals:
        return ret_str + decimals
    return ret_str

def dict_sum(dict1, dict2):
    '''
    字典求和
    '''
    dict_total = {}
    
    for k,v in dict1.items():
        if dict2.has_key(k):
            v += dict2[k]
            dict2.pop(k)
        dict_total[k] = v
    dict_total.update(dict2) 
    return dict_total

def str_2_low(x):
    if type(x) == types.StringType or type(x) == types.UnicodeType:
        return x.lower()
    return x

def sort_data(data, sort_fields, reverse):
    if sort_fields:
        #FIXME 怎样快捷地做多字段排序
        field0 = sort_fields[0]
        k = field0.keys()[0]
        v = field0[k]
        return sorted(data, key=lambda x:str_2_low(x['%s_key'%k]) if x.has_key('%s_key'%k) else str_2_low(x[k]) if x.has_key(k) else None, reverse=not v)
    elif reverse:
        data.reverse()
    return data

def format_terminal(os_str):
    if os_str == 'android':
        return 'Android'
    elif os_str == 'ios':
        return 'IOS'
    return ''

if __name__ == "__main__":
    assert num_readability(0) == ''
    assert num_readability(11001001) == '11,001,001'
    assert num_readability(11001001.01) == '11,001,001.01'
    assert num_readability(11001.20) == '11,001.2'
    assert num_readability(1) == '1'
    assert num_readability(1001) == '1,001'
    assert num_readability(21001) == '21,001'
    assert num_readability(121) == '121'
    assert num_readability(110010010001200213019491) == '110,010,010,001,200,213,019,491'
