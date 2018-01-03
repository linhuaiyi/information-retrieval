# -*- coding:utf-8 -*-
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

corpus = np.loadtxt('conversation\\response.index', delimiter=',', usecols=(1,), dtype='str')
#print corpus
#for sen in corpus:
#    b = eval(repr(sen))
#    print b.decode('gbk')
#    #b = repr(sen)
#    #print unicode(eval(b), "gbk")

#vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
#transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
#tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))  #  第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
##print tfidf
#print vectorizer.vocabulary_
#print transformer.idf_
#word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
##for word_in_wob in word:
##    print word_in_wob
#print type(tfidf)


tfidf_tran = TfidfVectorizer()
tfidf_from_tran = tfidf_tran.fit_transform(corpus)
#print tfidf_tran.vocabulary_
voc = tfidf_tran.vocabulary_
idf = tfidf_tran.idf_
fea = tfidf_tran.get_feature_names()
print tfidf_from_tran
line = 0
data_begin_index = tfidf_from_tran.indptr[line]
data_end_index = tfidf_from_tran.indptr[line + 1]
print tfidf_from_tran.indices[data_begin_index:data_end_index]
print tfidf_from_tran.data[data_begin_index:data_end_index]
print type(tfidf_from_tran)
print idf[124545]
#print type(voc)  # dict key is word, value is position in idf array and feature list
#print type(idf)  # np.array
#print type(fea)  # list
count_voc = 0
count_idf = 0
count_fea = 0
count_cmp = 0
f_v = open('voca.txt', 'w+')
for key, value in voc.items():
    count_voc += 1
    print >> f_v, key,
    print >> f_v, value
f_v.close()
#print count_voc  # 233120

f_i = open('idf.txt', 'w+')
for i in idf:
    count_idf += 1
    print >> f_i, i
f_i.close()
#print count_idf  # 233120

f_f = file('feature.txt', 'w+')
for a in fea:
    count_fea += 1
    print >> f_f, a
f_f.close()
#print count_fea  # 233120

#print tfidf_tran.idf_
#print type(tfidf_tran.get_feature_names())

new_file = ['祝', '汤', '教授', '新年', '快乐']
new_vecotr = [0 for _ in range(233120)]
for word in new_file:
    word = word.decode('utf-8')
    if word in voc:
        tf = 1
        pos = voc[word]
        idf_value = idf[pos]
        print idf_value
        new_vecotr[pos] = tf * idf_value
        print voc[word]
