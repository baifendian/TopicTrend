#encoding:utf-8
import sys
import jieba
import numpy as np
from gensim.models.word2vec import Word2Vec
from textrank4zh import TextRank4Keyword, TextRank4Sentence
reload(sys)
sys.setdefaultencoding('utf-8')
class GetSummary:
    def __init__(self, w2v_model_path):
        self.vec = Word2Vec.load(w2v_model_path)
    #flag为0表示提取关键词，flag为1表示提取关键句，关键词可能返回为空
    def get_summary(self, data, flag=0):
        text = "".join(data)
        if flag == 0:
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=text, lower=True, window=2)
            #ret = tr4w.get_keywords()
            ret = tr4w.get_keyphrases(keywords_num = 12, min_occur_num = 0)
            if len(ret) >= 0:
                return ret[0]
            else :
                return ""
        else :
            tr4s = TextRank4Sentence()
            tr4s.analyze(text=text, lower=True)
            ret = tr4s.get_key_sentences(num=6, sentence_min_len=4)
            if len(ret) >= 0:
                return ret[0]['sentence']
            else :
                return ""

    def get_vec(self, data, word2vec_model_path=None):
        words = jieba.cut(data)
        ret = np.zeros(100)
        #vec = Word2Vec.load(word2vec_model_path)
        for word in words:
            try:
                ret = ret + self.vec[word]
            except Exception as e:
                print >> sys.stderr, e
        return ret


if __name__ == "__main__":
    getsummary = GetSummary("model/word2vec_model")
    data = ['苹果现在喝口水能立马咽到小腹的感觉真通透','苹果肌浩瀚海洋，源于细小溪流；伟大成就，来自艰苦劳动', '苹果的分辨率太低，而且5屏幕太小，刚刚试了一下，的确没法看，是不是要换手机了', '苹果酸奶还有煮玉米，他生气说他不爱吃玉米，女人不高兴了，好心没有回报，便一头扎进卧继续睡...他走了，她继续睡...两三个小时后他电话来说正在吃玉米，好好吃...其实他只是不想她早起忙碌而已……','苹果肌*4、囧膜*2、旅行>套组*2准时开抢，赠品也太丰富了吧','苹果新闻资讯！投稿请私信：Q1375888','苹果iPhone中文网官方微博','苹果创意馆官网applefuns.com官方微博','>苹果、蚂蚁金服和中国人寿后又一重大投资方！-EZCapital中国创业投资第一在线交流平台6月22日，近日保利地产发布公告称，公司持有30%股权的合资公司','保利投资拟发起设立珠海利晖基金，预计规模拟定不超过25亿元人民币','公告显示，珠海利晖基金','苹果脆片---烤箱版】做法，详细步骤']
    ret = getsummary.get_summary(data, flag=0)
    print ret
    print getsummary.get_vec(ret)
