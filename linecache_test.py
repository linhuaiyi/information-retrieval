import linecache
import re

count = linecache.getline("conversation\\original.pair", 2)
count = re.split(',|\n', count.split(':')[1])[:-1]
print count
