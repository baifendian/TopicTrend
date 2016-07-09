#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, os, json, datetime, logging
from scipy import spatial

from mongodb_op import MongoOps
from bi_cluster import Cluster
from get_summary import GetSummary

class EventDetector(object):
    '''
        话题发现器
        使用聚类方法发现描述相同的话题或事件
    '''
    def __init__(self, cluster_model_file, vector_model_file):
        self.db = "crawldata"
        self.source_tables = ["weibo", "weixin", "news"]
        self.event_table = "event"
        self.record_table = "record"
        self.source_dic = {}
        self.mdb = MongoOps(self.db)
        self.cluster = Cluster(vector_model_file)
        self.summarize = GetSummary(vector_model_file)
        self.cluster_model_file = cluster_model_file
        self.vector_model_file = vector_model_file

    def insert_event(self, desc, vector, category, influence=0):
        '''新增话题表'''
        logging.info("insert into event table.")
        event = {"desc": desc, "vector":vector, "cate":category, "influence":influence}
        res = self.mdb.insert_one(self.event_table, event)        
        return res.inserted_id

    def get_last_day_event(self, date, category):
        '''获取昨天的话题'''
        last_day = datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=1)
        day_str = day_str = last_day.strftime("%Y-%m-%d")        
        query = {"date":day_str}
        cur = self.mdb.query(self.record_table, query)
        event_id = []
        for res in cur:
            event_id.append(res["event_id"])
            
        last_event = []
        for eid in event_id:
            cur = self.mdb.query_by_id(self.event_table, eid)
            for res in cur:
                if res["cate"] != category:
                    continue
                last_event.append([str(res["_id"]), res["desc"]])
        return last_event   
 
    def insert_record(self, date, event_id, influence=0):
        '''添加记录表'''
        logging.info("insert to record table")
        record = {"date":date, "event_id":event_id, "influence":influence}
        res = self.mdb.insert_one(self.record_table, record)
        return res
        

    def update_source(self, date, title, event_id):
        '''更新数据源表'''
        #logging.info("update data source table.")
        table = self.source_dic[title]
        query = {"date":date, "title":title}
        update = {"$set":{"event_id":event_id} }
        self.mdb.update_one(table, query, update)
    

    def get_source(self, date, e_cate):
        '''获取当天数据源'''
        docs = []
        for table in self.source_tables:
            if table == "news":
                query = {"date":date}
            else:
                query = {"date":date, "cate":1}
            cur = self.mdb.query(table, query)
            i = 0
            for res in cur:
                #if 'cate' in res and res['cate'] != 1:
                #    continue
                title = res['title']
                # TODO: 以后在配置文件里配置
                if e_cate == 0:
                    if u"iphone" in title or u'iPhone' in title or u"苹果" in title or u"小米" in title:
                        continue
                elif e_cate == 1:
                    if u"苹果" not in title:
                        continue
                elif e_cate == 2:
                    if u"小米" not in title:
                        continue
                elif e_cate == 3:
                    if u"iphone" not in title:
                        continue
                
                self.source_dic[title] = table
                #rid = str(res['_id'])
                docs.append(title)
                i += 1
            logging.info("get %d source from %s" %(i , table))
        return docs

    def process(self, date, cate, thre):
        '''主处理流程'''
        last_event = self.get_last_day_event(date, cate)
        logging.info("get last day event %d" %len(last_event))
        docs = self.get_source(date, cate)
        logging.info("there are %d docs" % len(docs))
        if cate == 0:
            threshold = 0.5
        elif cate == 2:
            threshold = 0.5
        else:
            threshold = 0.1
        #clustered = self.cluster.train_by_word2vec(docs, threshold=threshold)
        clustered = self.cluster.train_by_tfidf(docs,self.cluster_model_file,  threshold=threshold)
        for data in clustered:
            if len(data) == 1:
                continue
            #if len(data) > 70:
            #    continue
            logging.debug("new catgory **")
            logging.debug(json.dumps(data,ensure_ascii=False).encode("u8"))
            c_desc = self.summarize.get_summary(data)
            if c_desc == "":
                c_desc = self.summarize.get_summary(data, flag=1)
            vector = self.summarize.get_vec(c_desc)
            logging.debug("summary: %s" %c_desc)
            find_similarity = False
            for e_id, e_desc in last_event:
                e_vector = self.summarize.get_vec(e_desc)
                similarity = 1.0 - spatial.distance.cosine(vector, e_vector)
                logging.debug("%s ** %s ** %f" %(c_desc, e_desc, similarity))
                if similarity >= thre:
                    this_id = e_id
                    find_similarity = True
                    break
            if not find_similarity:
                this_id = self.insert_event(c_desc, [0.0], cate)
           
            this_id = str(this_id) 
            self.insert_record(date, this_id)
            for rec in data:
                self.update_source(date, rec, this_id) 


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print >> sys.stderr, "Usage: %s date" % sys.argv[0]
        sys.exit()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    date = sys.argv[1]
    detector = EventDetector("model/tfidf_model1", "model/word2vec_model")
    #detector.process(date, 0, 0.5)
    #detector.process(date, 1, 0.5)
    #detector.process(date, 2, 0.5)
    detector.process(date, 3, 0.5)
