# -*- coding:utf-8 -*-
import numpy as np
from io import StringIO

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

c = StringIO(unicode("0--223\n1--44"))
# stc = '0##哈哈哈哈'
# list = stc.split('##')
i, response_corpus = np.loadtxt(c, delimiter='--', usecols=(0, 1), dtype='str', unpack=True)
print response_corpus