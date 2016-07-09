#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, os ,json
from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoOps(object):
    def __init__(self, db, host=None):
        if host:
            self.client = MongoClient(host)
        else:
            self.client = MongoClient()

        self.db = self.client[db]

    def insert_one(self, table, data):
        result = self.db[table].insert_one(data)
        #print "insert ", json.dumps(data, ensure_ascii=False).encode("u8")
        return result

    def query(self, table, query):
        cursor = self.db[table].find(query)
        return cursor

    def update_one(self, table, query, update):
        result = self.db[table].update_one(query, update)
        return result

    def query_by_id(self, table, rec_id):
        if type(rec_id) == str:
            rid = ObjectId(rec_id)
        elif type(rec_id) == unicode:
            rid = ObjectId(str(rec_id))
        else:
            rid = rec_id
        #print rec_id, type(rec_id), rid, type(rid)
        cursor = self.db[table].find({"_id": rid})
        return cursor

if __name__ == '__main__':
    pass
        
