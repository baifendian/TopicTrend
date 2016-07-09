# -*- coding: UTF-8 -*-
'''
Created on 2014-8-04

@author: ward
'''
import types
from django.conf import settings
from pymongo import MongoClient

class MongoClassSimple(object):
    #index_field 表示索引字段，collection_list表示建哪些collection
    def __init__(self,db_name,addr=[],user=None,password=None):
        if addr:
            self.mongo_conn = MongoClient(addr)
        else:
            self.mongo_conn = MongoClient(settings.MONGO_ADDR) #默认连接到localhost,27017
        self.mongo_db = self.mongo_conn[db_name] 
    
    def count(self, resource, prec=None):
        if prec:
            return self.mongo_db[resource].count(prec)
        return self.mongo_db[resource].count()
    
    def insert_doc(self, resource, doc):
        if type(doc) == types.ListType:
            self.mongo_db[resource].insert_many(doc)
        else:
            self.mongo_db[resource].insert_one(doc)
    
    def update_doc(self, resource, prec, newpart):
        self.mongo_db[resource].update_many(prec, {"$set": newpart})
    
    def upsert_doc(self, resource, prec, newpart):
        self.mongo_db[resource].update(prec, {"$set": newpart}, upsert=True)
    
    def find_one_doc(self, resource, prec, ret_fields = None):
        return self.mongo_db[resource].find_one(prec, ret_fields) if ret_fields \
                else self.mongo_db[resource].find_one(prec) 
    
    def find_docs(self, resource, prec, ret_fields = None, sort_field = None, direction=1,limit_num = None,sort_fields=[]):
        cursor = self.mongo_db[resource].find(prec,ret_fields) if ret_fields \
                else self.mongo_db[resource].find(prec) 
        if sort_fields:
            cursor = cursor.sort(sort_fields)
        elif sort_field:
            cursor = cursor.sort(sort_field, direction)
        if limit_num:
            cursor = cursor.limit(limit_num)
        return cursor
    
    def find_distinct(self, resource, prec, field):
        return self.mongo_db[resource].distinct(field, prec)
    
    def group(self, resource, key, condition, initial, reduce, sort_field = None, limit_num = None):
        cursor = self.mongo_db[resource].group(key, condition, initial, reduce)
#         if sort_field:
#             cursor = cursor.sort(sort_field)
#         if limit_num:
#             cursor = cursor.limit(limit_num)
        return cursor
    
    def remove_docs(self, resource, prec):
        self.mongo_db[resource].remove(prec)
    
    def aggregate(self, resource, pipes, **kwargs):
        cursor = self.mongo_db[resource].aggregate(pipes)
        return cursor
    
    def close(self):
        self.mongo_conn.close()
