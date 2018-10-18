"""
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+
|  ~>>          K (Associahedron)          <<~  |
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+


"""

from utilities import *
from debug import *
import itertools as it

from CoxeterGraph import CoxeterGraph
from Polygon import Polygon

#
## K (Associahedron)
#
class K:

    def __init__(self, N):
        self.N = N
        self.coxeter_graph = CoxeterGraph(N)
        self.polygon = Polygon(N, self.coxeter_graph)

    def get_all_triangulations(self, i):
        return self.polygon.get_all_triangulations(i)