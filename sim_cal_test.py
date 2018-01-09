# -*- coding:utf-8 -*-

from corpus_to_tfidf import corpus_op
from stc_to_tfidf_vec import stc_to_vec
from sim_with_cor_stc import cal_sim

corpus_list_qr = ['conversation\\response.index', 'conversation\\post.index']
corpus_list_q = ['conversation\\post.index']
corpus_list_r = ['conversation\\response.index']
tf_idf_tran_qr, tf_idf_qr, size_list_qr = corpus_op(corpus_list_qr)
# tf_idf_tran_q, tf_idf_q, size_list_q = corpus_op(corpus_list_q)
# tf_idf_tran_r, tf_idf_r, size_list_r = corpus_op(corpus_list_r)

in_query = raw_input("Please input query:")
# Similarity calculate in corpus merged by q and r
# Similarity with r and p
tf_idf_vector = stc_to_vec(in_query, tf_idf_tran_qr)
line_sim_qr_dict, line_sim_qp_dict = cal_sim(tf_idf_vector, tf_idf_qr, size_list_qr)
