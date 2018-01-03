# -*- coding:utf-8 -*-
import numpy as np
from jieba_seg import jieba_stc_seg
from ltp_seg import ltp_stc_seg
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

response_corpus = np.loadtxt('conversation\\response.index', delimiter=',', usecols=(1,), dtype='str')
# print response_corpus
#  post_index, post_corpus =
tf_idf_tran = TfidfVectorizer()
tf_idf = tf_idf_tran.fit_transform(response_corpus)

voc = tf_idf_tran.vocabulary_
idf = tf_idf_tran.idf_
fea = tf_idf_tran.get_feature_names()

query = raw_input("Please input query:")
seg_result = ltp_stc_seg(query, "ws").split(" ")
query_seg_len = len(seg_result)
len_of_voc = len(voc)
tf_vector = np.zeros(len_of_voc)
idf_vector = np.zeros(len_of_voc)
for word in seg_result:
    word = word.decode('utf-8')
    if word in voc:
        pos = voc[word]  # word's position in vocabulary
        # print pos
        tf_vector[pos] += 1  # count terms of word
        idf_vector[pos] = idf[pos]  # get word's idf in record
tf_vector /= query_seg_len
tf_idf_vector = np.array(tf_vector*idf_vector)
# f = open('tf_idf_file', 'w+')
# for i in tf_idf_vector:
#     print >> f, i
corpus_size = len(tf_idf.indptr)
sim_rank_list = np.array([])
line_list = np.array([])
for line in range(corpus_size - 1):
    data_begin_index = tf_idf.indptr[line]
    data_end_index = tf_idf.indptr[line + 1]
    sim_score = 0
    for index, fea_index in enumerate(tf_idf.indices[data_begin_index:data_end_index]):
        if tf_idf_vector[fea_index] != 0:
            sim_score += tf_idf_vector[fea_index] * tf_idf.data[data_begin_index:data_end_index][index]
    if sim_score != 0:
        sim_rank_list = np.append(sim_rank_list, sim_score)
        line_list = np.append(line_list, line)
for sim_final_score, line in zip(sim_rank_list, line_list):
    print sim_final_score, response_corpus[int(line)]
print "finished !"

