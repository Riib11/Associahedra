"""
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+
|  ~>>              Utilities              <<~  |
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+


"""

from debug import *
import itertools as it

def inrange(a, b=None): # [a, ..., b] inclusive
    if not b: a, b = 1, a
    return [i for i in range(a, b + 1)]

def safemax(xs): return max(xs) if len(xs) > 0 else 1

# i is the number of flatten iterations
def flatten(xs, i=1):
    if i == 0: return xs
    else:
        xs_new = []
        for x in xs: xs_new += x
        return flatten(xs_new, i-1)