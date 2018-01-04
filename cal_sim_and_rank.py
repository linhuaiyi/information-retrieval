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
    # print response_corpus
    #  post_index, post_corpus =
    tf_idf_tran = TfidfVectorizer()
    tf_idf = tf_idf_tran.fit_transform(response_corpus)

    voc = tf_idf_tran.vocabulary_  # voc line in feature table
    idf = tf_idf_tran.idf_  # line:idf value
    # fea = tf_idf_tran.get_feature_names()

    # Sentence segment
    seg_result = ltp_stc_seg(query, "ws").split(" ")
    query_seg_len = len(seg_result)
    len_of_voc = len(voc)  # Vocabulary length
    tf_vector = np.zeros(len_of_voc)  # Vector with the length of vocabulary and each element store tf score
    idf_vector = np.zeros(len_of_voc)  # Vector with the length of vocabulary and each element store idf score
    for word in seg_result:
        word = word.decode('utf-8')
        if word in voc:
            pos = voc[word]  # word's position in vocabulary
            # print pos
            tf_vector[pos] += 1  # count terms of word
            idf_vector[pos] = idf[pos]  # get word's idf in record
    tf_vector /= query_seg_len
    # TF-IDF vector of query
    tf_idf_vector = np.array(tf_vector*idf_vector)
    # f = open('tf_idf_file', 'w+')
    # for i in tf_idf_vector:
    #     print >> f, i
    corpus_size = len(tf_idf.indptr) - 1
    sim_rank_list = np.array([])
    line_list = np.array([])
    # dot with each response vector
    for line in range(corpus_size):
        data_begin_index = tf_idf.indptr[line]
        data_end_index = tf_idf.indptr[line + 1]
        sim_score = 0
        for index, fea_index in enumerate(tf_idf.indices[data_begin_index:data_end_index]):
            if tf_idf_vector[fea_index] != 0:
                sim_score += tf_idf_vector[fea_index] * tf_idf.data[data_begin_index:data_end_index][index]
        if sim_score != 0:
            sim_rank_list = np.append(sim_rank_list, sim_score)  # similarity score
            line_list = np.append(line_list, line)  # response(or post) position in response.pair(or post.pair)

    if pattern == "qp":
        r_sim = np.array([])
        r_list = np.array([])
        for index, line in enumerate(line_list):
            q_to_r = linecache.getline("conversation\\original.pair", line + 1)
            q_to_r = re.split(',|\n', q_to_r.split(':')[1])[:-1]
            for response_line in q_to_r:
                r_sim = np.append(r_sim, sim_rank_list[index])
                r_list = np.append(r_list, response_line)
        return r_sim, r_list
    else:
        return sim_rank_list, line_list


    # for sim_final_score, line in zip(sim_rank_list, line_list):
    #     print sim_final_score, response_corpus[int(line)]
    # print "finished !"

if __name__ == '__main__':
    in_query = raw_input("Please input query:")
    path = 'response.index'
    split_symbol = '-,-'
    sim, res_list = cal_tf_idf_sim(in_query, path, split_symbol, "qr")
    f = open('sim_cal_result.txt', 'w+')
    for s, r in zip(sim, res_list):
        print >> f, s, r
