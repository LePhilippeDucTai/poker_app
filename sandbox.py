from collections import namedtuple, Counter
from operator import itemgetter
import itertools as it
from functools import reduce
d = Counter({9: 2, 4: 1, 10: 1, 2: 1, 11: 1, 8: 1})
d2 = Counter({11: 2, 9: 2, 6: 1, 2: 1, 8: 1})

ls = sorted(sorted([(key, value) for key, value in d.items()], reverse = True, key = itemgetter(0)), reverse = True, key = itemgetter(1))
iterator = it.accumulate(ls, func = lambda acc, x : (x[0], acc[1] + x[1]))
subit = it.takewhile(lambda x : x[1] <= 5, iterator)
print(list(subit))
print(d, d2, sep = '\n')
