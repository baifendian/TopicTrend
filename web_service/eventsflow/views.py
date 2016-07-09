# -*- coding: utf-8 -*-
#-----------------------
import logging
import traceback
from django.conf import settings
from bson.objectid import ObjectId

logger = logging.getLogger('access_log')

from basic.basic_response import DataPackage, BasicResponse, RC_CODES
from basic.dbclient import reports_client
from utils.response import jsonp_wrapped_response

CATE_MAP = {
    0: '其他科技类',
    1: '苹果',
    2: '小米',
    3: 'iphone',
}
SHOW_NUM = 10

def index(request):
    return events(request)
    
def events(request):
    """
    @summary: 查看某日事件top
    @param date: 日期
    """
    basic_response = BasicResponse()
    
    params = request.GET
    
    try:
        date_str = params.get('date', '').strip()
        if not date_str :
            basic_response.set_rc(RC_CODES['ERROR']).set_msg('date参数缺失')
            return jsonp_wrapped_response(params, basic_response)
            
        cursor = reports_client.find_docs('event', {}, {'desc':1, 'cate':1})
        all_events = {}
        for line in cursor:
            _id = str(line.pop('_id'))
            line['id'] = _id
            all_events[_id] = line
        
        base_fields = {'_id':0, 'event_id':1, 'influence': 1}
        cursor = reports_client.find_docs('record', {'date': date_str}, 
                                          base_fields, sort_field='influence',
                                          direction=-1, limit_num=10)
        
        data_bucket = []
        for line in cursor:
            event_id = line.get('event_id', '')
            try:
                event_obj = all_events[event_id]
                event_obj['influence'] = line['influence']
                data_bucket.append(event_obj)
            except:
                pass
        
        data_package = DataPackage(data_bucket)
        basic_response.set_rc(RC_CODES['SUCCESS']).set_data(data_package).set_msg('OK')
    except:
        logger.error(traceback.format_exc())
        basic_response.set_rc(RC_CODES['INTERNAL_ERROR']).set_msg('internal error')
    return jsonp_wrapped_response(params, basic_response)

def lifetime(request):
    """
    @summary: 查看事件生命周期
    @param id: 事件ID
    """
    basic_response = BasicResponse()
    
    params = request.GET
    
    try:
        event_id = params.get('id', '').strip()
        if not event_id :
            basic_response.set_rc(RC_CODES['ERROR']).set_msg('id参数缺失')
            return jsonp_wrapped_response(params, basic_response)
            
        event_detail = reports_client.find_one_doc('event', 
                            {'_id': ObjectId(event_id)}, {'desc':1, 'cate':1})
        event_detail.pop('_id')
        
        base_fields = {'_id':0, 'date':1, 'influence': 1}
        cursor = reports_client.find_docs('record', {'event_id': event_id}, 
                            base_fields, sort_field='date',
                            direction=1,)
        
        data_package = DataPackage() \
            .set_elements([line for line in cursor]) \
            .set_fields({'detail': event_detail})
        basic_response.set_rc(RC_CODES['SUCCESS']).set_data(data_package).set_msg('OK')
    except:
        logger.error(traceback.format_exc())
        basic_response.set_rc(RC_CODES['INTERNAL_ERROR']).set_msg('internal error')
    return jsonp_wrapped_response(params, basic_response)
