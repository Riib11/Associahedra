"""
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+
|  ~>>               Divide                <<~  |
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+


"""

from utilities import *
from debug import *
import itertools as it

#
### Divide
#
class Divide:
    def __init__(self, v1, v2):
        # sort vertices
        [self.v1, self.v2] = sorted([v1, v2])

    # is this divide's vertices contained in
    # a set of vertices?
    def is_contained_in_vertices(self, vs):
        return self.v1 in vs and self.v2 in vs

    def __eq__(self, other):
        return [self.v1, self.v2] == [other.v1, other.v2]

    def tostring(self):
        return "d("+str(self.v1)+","+str(self.v2)+")"
    __str__ = tostring
    __repr__ = tostring

    @staticmethod
    def get_divide_index_func(V):
        divides_ordering = [
            Divide(v1, v2) for v1, v2
            in it.combinations(inrange(0, V - 1), 2) ]

        # uses custom Divide equality
        def get_divide_index(d):
            assert ( isinstance(d, Divide) )
            assert ( d in divides_ordering )
            return divides_ordering.index(d)

        return get_divide_index
