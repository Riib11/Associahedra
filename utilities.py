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