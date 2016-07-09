#!/opt/Python-2.7/bin/python
# -*- coding:utf-8 -*-

import os, sys, json, re, datetime
import glob
from mongodb_op import MongoOps

pat = re.compile(u"([0-9]+)")
mongo_client = MongoOps("crawldata")
wx_doc = "weixin"
tech_doc = "news"

def proc_title(text):
    '''清洗内容'''
    text = text.replace("\\n", "").replace(" ", "").strip()
    return text

def proc_cont(text_lst):
    '''清洗标题'''
    text_lst = [s.replace("\\n","").replace("\\t","").strip() for s in text_lst]
    return "".join(text_lst)

def date_format(date_str):
    date = datetime.datetime.strptime(date_str, "%Y%m%d")
    date_str = date.strftime("%Y-%m-%d")
    return date_str

def get_history_titles(date_str, table, days=3):
    '''获取历史标题数据'''
    date = datetime.datetime.strptime(date_str, "%Y%m%d")
    titles = []
    for d in xrange(1, days):
        this_day = (date-datetime.timedelta(days=d)).strftime("%Y-%m-%d")
        query = {'date': this_day}
        cur = mongo_client.query(table, query)
        for res in cur:
            #print res['title'].encode('u8')
            titles.append(res['title'])
    print "old titles:", len(titles)
    return titles

def proc_weixin_top(date, data_dir, uniq_before=False):
    '''清洗微信TOP数据'''
    if uniq_before:
        titles = get_history_titles(date, wx_doc, days=3)
    else:
        titles = list()
    for fn in glob.glob(os.path.join(data_dir,  "weixin_" + date + "*")):
        print "***", fn
        with open(fn, "r") as rf:
            for line in rf:
                data = json.loads(line.strip()) 
                if data['cate'].startswith('pc_0'):
                    continue
                title = proc_title(data['title'])
                if title in titles:
                    continue
                titles.append(title)
                cont = proc_cont(data['cont'])
                comment = 0
                match = pat.search(data['comment'])
                if match:
                    comment = int(match.group(1))
                record = {'date': date_format(date), 'title': title, 'cont': cont, 'cate':0, "read": comment}
                res = mongo_client.insert_one(wx_doc, record)
                #print json.dumps(record, ensure_ascii=False).encode("u8")

def proc_weixin_kw(date, data_dir, uniq_before=False):
    '''清洗微信关键词数据'''
    if uniq_before:
        titles = get_history_titles(date, wx_doc, days=3)
    else:
        titles = list()
    for fn in glob.glob(os.path.join(data_dir,  "weixin_" + date + "*")):
        print "***", fn
        with open(fn, "r") as rf:
            for line in rf:
                data = json.loads(line.strip())
                title = proc_title(data['title'])
                if title in titles:
                    continue
                date = data['date']
                cont = proc_cont(data['cont'])
                read = 0
                if 'readnum' in data:
                    if data['readnum'].endswith('+'):
                        read = 100000
                    else:
                        read = int(data['readnum'])
                record = {'date': date, 'title': title, 'cont': cont, 'cate':0, "read": read}
                res = mongo_client.insert_one(wx_doc, record)

def proc_tech_news(date, data_dir):
    '''处理科技新闻数据'''
    for fn in glob.glob(os.path.join(data_dir, "tech_" + date + "*")):
        print "****", fn
        with open(fn, "r") as rf:
            for line in rf:
                data = json.loads(line.strip())
                title = data['title']
                cont = proc_cont(data['content'])
                record = {'date': date_format(date), 'title': title, 'cont': cont, 'cate': 0}
                res = mongo_client.insert_one(tech_doc, record)
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        date = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y%m%d")
    else:
        date = sys.argv[1]
    
    print "process", date
    proc_weixin_kw(date, "../result_kw", uniq_before=True)
    proc_tech_news(date, "../result_tech")
    proc_weixin_top(date, "../result", uniq_before=True)

