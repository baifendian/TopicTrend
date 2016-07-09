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
           roots.add(self.find(i))
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
            if isinstance(word, str):
                word = word.decode('utf-8')
            word_num.setdefault(word, 0)
            word_num[word] = word_num[word] + 1
            line_len = line_len + 1
        for key in word_num.keys():
            if self.tfidf_model_dict.has_key(key):
                vec.append((self.tfidf_model_dict[key][0], word_num[key] * 1.0 / line_len * self.tfidf_model_dict[key][1]))
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
            if isinstance(line, str):
                line = line.decode('utf-8')
            if len(line) > 5:
                self.sentence.append(line)
                idx = idx + 1
        sentence_len = len(self.sentence)
        for i in range(sentence_len):
            for j in range(i + 1, sentence_len):
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
                self.tfidf_model_dict[items[0].decode('utf-8')] = (idx, float(items[1].replace("\n", "")))
                idx = idx + 1
        idx = 0
        for line in data:
            if len(line) > 5:
                self.sentence.append(line)
                self.tfidf_sparse.append(self.get_tfidf(line))
                idx = idx + 1
        tfidf_sparse_length = len(self.tfidf_sparse)
        for i in range(tfidf_sparse_length):
            for j in range(i + 1, tfidf_sparse_length):
                similary = self.get_similary(i, j)
                if similary > threshold:
                    self.union(i, j, threshold, 1)
        return self.myprint(idx)
if __name__ == "__main__":
    cluster = Cluster("./word2vec_model")
    in_data = open("07_05_keyword_clean", 'r')
    out_data1 = open("cluster_ret1", 'w')
    out_data2 = open('cluster_ret2', 'w')
    data = []
    for item in in_data:
        data.append(item)
    ret = cluster.train_by_tfidf(data, 'tfidf_model2', threshold=0.15)
    for item in ret:
        out_data1.write("=====================\n")
        for i in item:
            out_data1.write(i + "\n")
    ret = cluster.train_by_word2vec(data, threshold=0.5)
    for item in ret:
        out_data2.write("========================\n")
        for i in item:
            out_data2.write(i + '\n')
    in_data.close()
    out_data1.close()
    out_data2.close()
	
