#encoding:utf-8
import sys
import math
import jieba
import numpy as np
from gensim.models.word2vec import Word2Vec
reload(sys)
sys.setdefaultencoding('utf-8')
class Cluster:
    def __init__(self, word2vec_path=""):
        self.sentence = []
        self.tfidf_sparse = []
        self.bi_set = [-1 for i in range(1000000)]
        self.tfidf_model_dict = {}
        if word2vec_path != "":
            self.word2vec_model = Word2Vec.load(word2vec_path)        

    def find(self, idx):
        if self.bi_set[idx] == -1:
            return idx
        self.bi_set[idx] = self.find(self.bi_set[idx])
        return self.bi_set[idx]

    def union(self, idx1, idx2, threshold, flag):
        root1 = self.find(idx1)
        root2 = self.find(idx2)
        if flag == 1:
            similary = self.get_similary(root1, root2)
        else:
            similary = self.get_similary_by_word2vec(root1, root2)
        if root1 != root2 and similary > threshold:
             self.bi_set[root1] = root2

    def myprint(self, data_number):
       roots = set()
       ret = []
       for i in range(data_number):
           self.find(i)
           roots.add(self.bi_set[i])
       for i in roots:
           item = []
           for j in range(data_number):
               if self.bi_set[j] == i or j == i:
                   item.append(self.sentence[j])
           ret.append(item)
       return ret 

    #tfidf_model_dict为{word:(index, idf)}
    def get_tfidf(self, line):
        vec = []
        word_num = {}
        words = jieba.cut(line)
        line_len = 0
        for word in words:
            word_num.setdefault(word, 0)
            word_num[word] = word_num[word] + 1
            line_len = line_len + 1
        for key in word_num:
            if self.tfidf_model_dict.has_key(key):
                vec.append((self.tfidf_model_dict[key][0], word_num[key] * 1.0 / line_len * self.tfidf_model_dict[key][1]))
#        print vec
        return vec

    def get_similary(self, idx1, idx2):
        vec1 = self.tfidf_sparse[idx1]
        vec2 = self.tfidf_sparse[idx2]
        vec1.sort(lambda x, y: cmp(x[0], y[0]))
        vec2.sort(lambda x, y: cmp(x[0], y[0]))
        vec_len1 = len(vec1)
        vec_len2 = len(vec2)
        i = j = ret = 0
        while i < vec_len1 and j < vec_len2:
            if vec1[i][0] < vec2[j][0]:
                i = i + 1
            elif vec1[i][0] > vec2[j][0]:
                j = j + 1
            else:
                ret = ret + vec1[i][1] * vec2[j][1]
                i = i + 1
                j = j + 1
        mode1 = mode2 = 0
        for item in vec1:
            mode1 = mode1 + item[1] * item[1]
        for item in vec2:
            mode2 = mode2 + item[1] * item[1]
        if mode1 == 0 or mode2 == 0:
            return 0
        return ret * 1.0 / (math.sqrt(mode1) * math.sqrt(mode2))
    
    def get_word2vec(self, line):
        words = jieba.cut(line)
        ret = np.zeros(100)
        for word in words:
            try:
                ret = ret + self.word2vec_model[word]
            except:
                pass
#               print "%s is not key to word2vec model"%word
        return ret

    def get_similary_by_word2vec(self, idx1, idx2):
        sentence1 = self.sentence[idx1]
        sentence2 = self.sentence[idx2]
        x = self.get_word2vec(sentence1)
        y = self.get_word2vec(sentence2)
        return x.dot(y) / ((np.sqrt(x.dot(x))) * (np.sqrt(y.dot(y)))) 
    
    def train_by_word2vec(self, data, threshold=0.1):
        idx = 0
        for line in data:
            if len(line) > 5:
                self.sentence.append(line)
                idx = idx + 1
        for i in range(len(self.sentence)):
            for j in range(i + 1, len(self.sentence)):
                similary = self.get_similary_by_word2vec(i, j)
                if similary > threshold:
                    self.union(i, j, threshold, 0)
        return self.myprint(idx)

    def train_by_tfidf(self, data, tfidf_model_path, threshold=0.1):
        input_tfidf_model = open(tfidf_model_path, 'r')
        idx = 0
        for item in input_tfidf_model:
            items = item.split(" ")
            if len(items) == 2:
                self.tfidf_model_dict[items[0]] = (idx, float(items[1].replace("\n", "")))
                idx = idx + 1
        idx = 0
        for line in data:
            if len(line) > 5:
                self.sentence.append(line)
                self.tfidf_sparse.append(self.get_tfidf(line))
                idx = idx + 1
        for item in self.tfidf_sparse:
            print item
        for i in range(len(self.tfidf_sparse)):
            for j in range(i + 1, len(self.tfidf_sparse)):
                similary = self.get_similary(i, j)
                print similary
                if similary > threshold:
                    self.union(i, j, threshold, 1)
        return self.myprint(idx)
if __name__ == "__main__":
    cluster = Cluster("./word2vec_model")
    data = ['果新闻简介：小时苹果新闻资讯！投稿请私信','果中文网微博机构认证微博机构认证苹果中文网官方微博','果创意馆微博机构认证微博机构认证苹果创意馆官网官方微博找人关系链找人关系链','果苹果主演：文素丽金泰佑李善均评分：人赞兴趣直达区景点','果园地铁站北京地铁一号线地铁苹果签到人数人赞','石老蔡发表了博文揭底无人驾驶车：三大件成本起码万美元来源：第一财经特斯拉的拥有者永远不会认为它有什么问题，就好像苹果的粉丝会不假思索地排队购买一样。一名特斯拉车主对第一财经记者表','底无人驾驶车：三大件成本起码万美元来源：第一财经特斯拉的拥有者永远不会认为它有什么问题，就好像苹果的粉丝会不假思索地排队购买一样。一名特斯拉车主对第一财经记者表示。但随着的自动驾驶夺命车祸日>发布者：穿石老蔡','利君高利君每天起床的原因不是睡醒了，而是妈呀我好饿我的面包牛奶饼干鸡蛋苹果等着我宠幸呢馋嘴馋嘴然后就神清气爽的起来了酷酷','千雨千千雨给苹果手机充电的正确方法笑笑','奕小奕刚开始认识苹果的时候，它还比较小，我还能够抱它。现在长大了，我都抱不动了。小苹果变成了大苹果，希望时间停留在现在，你不在长大该多好呢。图片多余一张只显示音频视频的九宫格','博会员：孩子李波很多人跟我说别买国货，微软苹果之类质量还是好些，我看全世界都一样，有时人家还离谱些','果新闻简介：小时苹果新闻资讯！投稿请私信','果中文网微博机构认证微博机构认证苹果中文网官方微博','果园地铁站北京地铁一号线地铁苹果签到人数人赞','食日记早上火龙果奇艺果苹果汁中午芦笋紫甘蓝粥配肉松','人【好书记年劈山开路植树育林万亩荒山变成花果山】山东省蓬莱市南官山村书记吴长洲，带领乡亲们劈山开路修出多公里的山路，村里的苹果出山，户均收入万多元。路通了，他又带着村民绿化荒山，办起农家乐。>年里，吴长洲领着大伙干出现实版的山乡巨变']
    ret = cluster.train_by_tfidf(data, 'tfidf_model', threshold=0.8)
    for item in ret:
        print "====================="
        for i in item:
            print i
    print "******************************************"
    ret = cluster.train_by_word2vec(data, threshold=0.5)
    for item in ret:
        print "========================"
        for i in item:
            print i

