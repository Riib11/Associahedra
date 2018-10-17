from CoxeterGraph import CoxeterGraph
from Polygon import Polygon

#
## K (Associahedron)
#
class K:

    def __init__(self, N):
        self.N = N
        coxeter_graph  = CoxeterGraph(N)
        polygon        = Polygon(N, coxeter_graph)

    def get_all_triangulations(self, dim):
        return self.polygon.get_all_triangulations(dim)