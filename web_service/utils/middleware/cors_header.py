'''
Created on 2016-7-9

@author: ward
'''
import logging

logger = logging.getLogger('access_log')

class CORSMiddleware(object):
    """
    
    """
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        return response
    