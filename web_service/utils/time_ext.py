# -*- coding: UTF-8 -*-
'''
Created on 2015-6-5

@author: ward
'''
import time
import types
import json

hour_list = ['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00',
           '11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00']

def time_readability(seconds):
    '''
    把秒变得更加易读。
    改成递归更简洁
    '''
    seconds = int(seconds)
    if not seconds :
        return ''
    if seconds >= 60 :
        mins = seconds/60
        left_seconds = seconds%60
        suffix = '%s秒'%left_seconds if left_seconds else ''
        if mins >= 60:
            hours = mins/60
            left_mins = mins%60
            suffix = ('%s分钟'%left_mins if left_mins else '') + suffix
            if hours >= 24:
                days = hours/24
                left_hours = hours%24
                suffix = ('%s小时'%left_hours if left_hours else '') + suffix
                return '%s天%s'%(days,suffix)
            return '%s小时%s'%(hours,suffix)
        return '%s分钟%s'%(mins,suffix)
    return '%s秒'%seconds

def generate_full_ranger(start, end, granularity, reverse=False):
    start_stmp = time.mktime(time.strptime(start, "%Y-%m-%d"))
    end_stmp = time.mktime(time.strptime(end, "%Y-%m-%d"))

    full_ranger = []
    if granularity == 'hour':
        if start_stmp == end_stmp:
            full_ranger = ['%s %s'%(start,h) for h in hour_list]
        else:
            while start_stmp <= end_stmp:
                day_str = time.strftime("%Y-%m-%d", time.localtime(start_stmp))
                for h in hour_list:
                    full_ranger.append('%s %s'%(day_str,h))
                start_stmp += 24*3600
    elif granularity == 'week':
        while start_stmp <= end_stmp:
            _localtime = time.localtime(start_stmp)
            if _localtime.tm_wday == 0:
                full_ranger.append(time.strftime("%Y-%m-%d", _localtime))
            start_stmp += 24*3600
            # 可以修正为+6天
    elif granularity == 'month':
        while start_stmp <= end_stmp:
            _localtime = time.localtime(start_stmp)
            if _localtime.tm_mday == 1:
                full_ranger.append(time.strftime("%Y-%m-%d", _localtime))
            start_stmp += 24*3600
    else:
        # 默认按日期处理
        while start_stmp <= end_stmp:
            full_ranger.append(time.strftime("%Y-%m-%d", time.localtime(start_stmp)))
            start_stmp += 24*3600
    if reverse:full_ranger.reverse()
    return full_ranger 

def fix_ranger_whih_count(start, end, granularity, max_count):
    '''
    补全时间，当时间范围内产生的点数小于给定的数量时，qi始时间往前移动
    裁剪时间，当时间范围内产生的点数大于给定的数量时，qi始时间往后移动
    '''
    start_stmp = time.mktime(time.strptime(start, "%Y-%m-%d"))
    end_stmp = time.mktime(time.strptime(end, "%Y-%m-%d"))
    final_start = start 
    if granularity == 'week':
        first_monday = None
        week_count = 0
        while start_stmp <= end_stmp:
            _localtime = time.localtime(start_stmp)
            if _localtime.tm_wday == 0:
                if not first_monday:
                    first_monday = start_stmp
                week_count += 1
                start_stmp += 7*24*3600
                continue
            start_stmp += 24*3600
        
        # print time.strftime("%Y-%m-%d", time.localtime(first_monday)),week_count
        if not first_monday:
            # 传过来的数据有问题，不进行修正
            return final_start, end
        
        _final_start = first_monday - 7*24*3600*(max_count-week_count)
        final_start = time.strftime("%Y-%m-%d", time.localtime(_final_start))
    elif granularity == 'month':
        start_year = int(start[0:4])
        start_month = int(start[5:7])
        start_day = int(start[8:10])
        
        end_year = int(end[0:4])
        end_month = int(end[5:7])
        month_list = []
        
        while (start_year<end_year) or (start_year == end_year and start_month <= end_month):
            if start_day != 1:
                start_day = 1
                if start_month == 12:
                    start_month = 1
                    start_year += 1
                else:
                    start_month += 1
                continue
            month_list.append('%s-%s-01'%(start_year, start_month))
            
            if start_month == 12:
                start_month = 1
                start_year += 1
            else:
                start_month += 1
        
        final_start = month_list[len(month_list)-max_count]
    return final_start, end

def check_latest_ranger(dateTime):
    '''
    判断是最近几天
    '''
    yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time()-24*3600))
    if type(dateTime) == types.DictType and dateTime['$lte'] == yesterday:
        lte = time.strptime(yesterday, '%Y-%m-%d')
        gte = time.strptime(dateTime['$gte'], '%Y-%m-%d')
        distance = int(time.mktime(lte)-time.mktime(gte))/24/3600
        return distance+1
    return None
            
def get_ranger_distance(dateTime):
    '''
    判断几天
    '''
    if type(dateTime) == types.DictType:
        lte = time.strptime(dateTime['$lte'], '%Y-%m-%d')
        gte = time.strptime(dateTime['$gte'], '%Y-%m-%d')
        distance = int(time.mktime(lte)-time.mktime(gte))/24/3600
        return dateTime['$lte'], distance
    else:
        return dateTime, 0

def handle_datetime(data_str, data_name):
    if data_str and data_name:
        try:
            data_obj = json.loads(data_str)
            if data_obj and types.ListType == type(data_obj):
                if len(data_obj) == 1:
                    return {'%s' %data_name:data_obj[0]}
                return {'%s' %data_name:{'$in':data_obj}}
            else :
                raise ValueError('param %s is not json' %data_name)
        except:
            raise ValueError('param %s is not json' %data_name)
    return {}

def check_ranger(ranger):
    return True

def handle_ranger(ranger_str):
    if ranger_str:
        try:
            ranger = json.loads(ranger_str)
            if types.ListType == type(ranger) and check_ranger(ranger):
                if ranger[0] == ranger[1]:
                    return {'dateTime' :ranger[0]}
#                     return {'dateTime' :ranger[0] + " 00:00:00"}
                return {'dateTime' :{'$gte':ranger[0], '$lte':ranger[1]}}
            else :
                raise ValueError('param ranger is not array' )
        except:
            raise ValueError('param ranger is not array' )
    return {}

if __name__ == "__main__":
    print time_readability(0)
    print time_readability(45)
    print time_readability(60)
    print time_readability(145)
    print time_readability(60*61)
    print time_readability(60*61*24)
    
    print generate_full_ranger('2015-05-20', '2015-06-20', 'week')
    print generate_full_ranger('2015-05-18', '2015-05-20', 'week')
    print generate_full_ranger('2015-05-20', '2015-06-20', 'month')
    print generate_full_ranger('2015-05-20', '2015-08-20', 'month')
    print generate_full_ranger('2015-05-01', '2015-07-01', 'month')
    print generate_full_ranger('2015-05-20', '2015-06-20', 'day')
    
    print fix_ranger_whih_count('2015-06-20', '2015-06-25', 'week', 1)
    print fix_ranger_whih_count('2015-06-20', '2015-06-25', 'week', 2)
    print fix_ranger_whih_count('2015-06-20', '2015-06-25', 'week', 3)
    print fix_ranger_whih_count('2015-06-20', '2015-06-22', 'week', 2)
    
    print '============test month============='
    print fix_ranger_whih_count('2015-06-05', '2015-08-01', 'month', 1)
    print fix_ranger_whih_count('2015-06-05', '2015-08-02', 'month', 2)
    print fix_ranger_whih_count('2015-06-05', '2015-08-31', 'month', 1)
    print fix_ranger_whih_count('2015-06-01', '2015-08-02', 'month', 1)
    print fix_ranger_whih_count('2015-06-01', '2015-08-01', 'month', 1)
    
