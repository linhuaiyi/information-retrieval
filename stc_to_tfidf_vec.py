# -*- coding:utf-8 -*-

import numpy as np
from jieba_seg import jieba_stc_seg
from ltp_seg import ltp_stc_seg
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# Merge corpus includes post and response
# and map them into same word space
def stc_to_vec(stc, tf_idf_tran):
    voc = tf_idf_tran.vocabulary_  # voc mapping , type is dict
    idf = tf_idf_tran.idf_

    # Split sentence input
    stc_seg_result = ltp_stc_seg(stc, "ws").split(" ")
    len_of_voc = len(voc)  # Vocabulary length
    tf_vector = np.zeros(len_of_voc)  # Vector with the length of vocabulary and each element store tf score
    idf_vector = np.zeros(len_of_voc)  # Vector with the length of vocabulary and each element store idf score
    stc_seg_len = len(stc_seg_result)  # the number of words from segment of sentence

    for word in stc_seg_result:
        word = word.decode('utf-8')
        if word in voc:
            pos = voc[word]  # word's position in feature of vector
            tf_vector[pos] += 1  # count terms of word
            idf_vector[pos] = idf[pos]  # get word's idf in record

    tf_vector /= stc_seg_len
    tf_idf_vector = np.array(tf_vector * idf_vector)

    return tf_idf_vector
