#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, os, json, logging

import cPickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing  import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfTransformer
import jieba

from mongodb_op import MongoOps

class Train(object):
    '''
        训练分类器，区分目标文档和非目标文档
    '''
    def __init__(self, stop_file=None, use_tfidf=False):
        self.stop_words = ["", " "]
        if stop_file:
            with open(stop_file, 'r') as rf:
                tokens = rf.readlines()
                tokens = [t.strip().decode("u8") for t in tokens]
                self.stop_words.extend(tokens)
                print "*****"
                logging.info("load %d stop words" % len(self.stop_words))
        jieba.initialize()
        self.label_encoder = LabelEncoder()
        if use_tfidf:
            self.pipeline = Pipeline([
                        ('vec',   CountVectorizer(stop_words=self.stop_words)),
                        ('feat',  TfidfTransformer()),
                        #('clf', SGDClassifier())
                        ('clf', MultinomialNB())
                 ])
        else:
            self.pipeline = Pipeline([
                        ('vec',   CountVectorizer(stop_words=self.stop_words, binary=True)),
                        ('clf',   BernoulliNB(fit_prior=True))
                 ])
        logging.info("init the classifier")     

    def segment(self, text):
        seg_list = jieba.cut(text)
        return u" ".join(seg_list)
        #return list(seg_list)

    def train(self, texts, labels):
        texts = [self.segment(t) for t in texts]
        y = self.label_encoder.fit_transform(labels)
        self.pipeline.fit(texts, y)
        
    def save_model(self, dumpfile):
        self.model = (self.pipeline, self.label_encoder)
        with open(dumpfile, 'wb') as f:
           cPickle.dump(self.model, f)

    def get_model(self):
        return self.pipeline, self.label_encoder

class Predict(object):
    '''
        使用模型预测文档分类
    '''
    def __init__(self, model=None, model_file=None):
        if model:
            self.pipeline, self.label_encoder = model
        elif model_file:
            self.load_model(model_file)
        else:
            raise Exception("param model or model_file should be passed")
        jieba.initialize()
        logging.info("predictor init sucessfully.")
    
    def segment(self, text):
        seg_list = jieba.cut(text)
        return u" ".join(seg_list)
        #return list(seg_list)

    def predict(self, texts):
        texts = [self.segment(t) for t in texts]
        y = self.pipeline.predict(texts)
        result = self.label_encoder.inverse_transform(y)
        return result

    def load_model(self, model_file):
        fp = open(model_file, "r")
        (self.pipeline, self.label_encoder) = cPickle.load(fp)
        fp.close()

def train(data_file, model_file, stop_file, split_ratio=0.1, use_tfidf=True):
    '''训练函数'''
    trainer = Train(stop_file=stop_file, use_tfidf=use_tfidf)
    texts = []
    labels = []
    with open(data_file) as df:
        for line in df: 
            label , text = line.strip().decode("u8").split("\t")
            labels.append(label) 
            texts.append(text)   
            
    if split_ratio > 1e-4:
        evaluation = True
        train_text, test_text, train_label, test_label = train_test_split(texts, labels, test_size=split_ratio, random_state=42)
    else:
        train_text, train_label = texts, labels

    logging.info("start to train...")
    trainer.train(train_text, train_label)
    trainer.save_model(model_file)
    logging.info("train done.")
    
    if evaluation:
        predictor = Predict(trainer.get_model())
        preds = predictor.predict(test_text)
        print(classification_report(test_label, preds, target_names=['not tech', 'tech']))

def predict(model_file, date, table):
    '''预测函数'''
    predictor = Predict(model_file=model_file)
    query = {"date": date}
    mongo_ops = MongoOps("crawldata")

    cur = mongo_ops.query(table, query)
    logging.info("get %d docs" % cur.count())
    for res in cur:
        title = res['title']
        cont = u""
        if "cont" in res:
            cont = res['cont']
        pred = predictor.predict([title+u" "+cont])
        cate = int(pred[0])
        query = {'date':date, 'title':title}
        update = {"$set": {"cate":cate}}
        mongo_ops.update_one(table, query, update)
        print pred, title.encode("u8")
        

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print >> sys.stderr, "Usage: %s train <model_file> <data_file> 0-document/1-title \
                            \n\t predict <model_file> date weixin/weibo" % sys.argv[0]
        sys.exit()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    if sys.argv[1] == "train":
        if sys.argv[4] == '0':
            use_tfidf = True
        else:
            use_tfidf = False
        train(sys.argv[3], sys.argv[2], "data/stop_words", 0.1, use_tfidf)
    elif sys.argv[1] == "predict":
        predict(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print >> sys.stderr, "Unkown parameter: %s" %sys.argv[1]
        
