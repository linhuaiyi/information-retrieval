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


def cal_sim(tf_idf_vector, tf_idf, size_list_qr):
    # Similarity features dict for further calculate
    line_sim_qr_dict = {}  # key is line
    line_sim_qp_dict = {}  #
    corpus_size = len(tf_idf.indptr)

    for line in range(corpus_size - 1):
        data_begin_index = tf_idf.indptr[line]
        data_end_index = tf_idf.indptr[line + 1]
        sim_score = 0
        for index, fea_index in enumerate(tf_idf.indices[data_begin_index:data_end_index]):
            if tf_idf_vector[fea_index] != 0:
                sim_score += tf_idf_vector[fea_index] * tf_idf.data[data_begin_index:data_end_index][index]
        if sim_score != 0 and line < size_list_qr[0]:  # line scope in response's range
            line_sim_qr_dict[line] = sim_score  # add line as key and similarity score as value in qr dict
        elif sim_score != 0 and line >= size_list_qr[0]:  # line scope in post's range
            line_in_post = line - size_list_qr[0]
            # Get responses relate with post
            q_to_r = linecache.getline("conversation\\original.pair", int(line_in_post + 1))
            q_to_r = re.split(',|\n', q_to_r.split(':')[1])[:-1]
            for response_line in q_to_r:
                line_sim_qp_dict[response_line] = sim_score  # add line as key and similarity score as value in qp dict
    return line_sim_qr_dict, line_sim_qp_dict


def cal_sim_bad(tf_idf_vector, tf_idf, size_list_qr):
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

    if size_list_qr.size > 1:
        r_list = np.array([])
        for index, line in enumerate(line_list):
            q_to_r = linecache.getline("conversation\\original.pair", line + 1)
            q_to_r = re.split(',|\n', q_to_r.split(':')[1])[:-1]
            for response_line in q_to_r:
                r_sim = sim_rank_list[index]
                r_list = np.append(r_list, response_line)
        return r_sim, r_list
    return sim_rank_list, line_list
    # for sim_final_score, line in zip(sim_rank_list, line_list):
    #     print sim_final_score, response_corpus[int(line)]
    # print "finished !"
