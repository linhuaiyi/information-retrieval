# -*- coding:utf-8 -*-

import jieba


def jieba_stc_seg(text):
    return " ".join(jieba.cut(text))
