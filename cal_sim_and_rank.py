# -*- coding:utf-8 -*-
import re
import numpy as np
import linecache
from jieba_seg import jieba_stc_seg
from ltp_seg import ltp_stc_seg
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def cal_tf_idf_sim(query, file_path, delimiter='-,-', pattern="qr"):
    response_corpus = np.loadtxt(file_path, delimiter=delimiter, usecols=(1,), dtype='str')
    # print response_corpus  # <type 'numpy.ndarray'>
    #  post_index, post_corpus =
    tf_idf_tran = TfidfVectorizer()
    tf_idf = tf_idf_tran.fit_transform(response_corpus)
    print tf_idf
    voc = tf_idf_tran.vocabulary_  # voc mapping
    idf = tf_idf_tran.idf_
    # fea = tf_idf_tran.get_feature_names()

    seg_result = ltp_stc_seg(query, "ws").split(" ")
    query_seg_len = len(seg_result)
    len_of_voc = len(voc)  # Vocabulary length
    tf_vector = np.zeros(len_of_voc)  # Vector with the length of vocabulary and each element store tf score
    idf_vector = np.zeros(len_of_voc)  # Vector with the length of vocabulary and each element store idf score
    for word in seg_result:
        word = word.decode('utf-8')
        if word in voc:
            pos = voc[word]  # word's position in feature of vector
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
    # dot with each response vector
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

    if pattern == "qp":
        r_list = np.array([])
        for index, line in enumerate(line_list):
            q_to_r = linecache.getline("conversation\\original.pair", line + 1)
            q_to_r = re.split(',|\n', q_to_r.split(':')[1])[:-1]
            for response_line in q_to_r:
                r_sim = sim_rank_list[index]
                r_list = np.append(r_list, response_line)
    # for sim_final_score, line in zip(sim_rank_list, line_list):
    #     print sim_final_score, response_corpus[int(line)]
    # print "finished !"

if __name__ == '__main__':
    in_query = raw_input("Please input query:")
    path = 'conversation\\response.index'
    split_symbol = '-,-'
    cal_tf_idf_sim(in_query, path, split_symbol, "qr")
