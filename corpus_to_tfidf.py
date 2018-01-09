# -*- coding: utf-8 -*-

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def corpus_op(corpus_file_list, delimiter='-,-'):
    # Merge corpus
    size_list = np.array([])
    corpus = np.array([])
    for file_path in corpus_file_list:
        tmp_size = corpus.size
        corpus = np.append(corpus, np.loadtxt(file_path, delimiter=delimiter, usecols=(1,), dtype='str'))
        size_list = np.append(size_list, corpus.size - tmp_size)
    tf_idf_tran = TfidfVectorizer()
    tf_idf = tf_idf_tran.fit_transform(corpus)

    return tf_idf_tran, tf_idf, size_list
