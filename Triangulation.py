"""
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+
|  ~>>            Triangulation            <<~  |
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+


"""

from utilities import *
from debug import *
import itertools as it

from Divide import Divide

#
### Triangulation
#
class Triangulation:
    def __init__(self, N, ds, polygon, coxeter_graph, 
        get_divide_index # Divide -> Index
    ):
        assert ( polygon.is_valid_triangulation(ds) )

        self.N = N
        self.ds = sorted(ds, key=get_divide_index)
        self.polygon = polygon
        self.coxeter_graph = coxeter_graph

    def tostring(self): return "Tri"+str(self.ds)
    __str__ = tostring
    __repr__ = tostring

    # this triangulation has all of
    # divides ds
    def has_divides(self, ds):
        assert ( all([isinstance(d, Divide) for d in ds]) )
        return all([ d in self.ds for d in ds ])

    # both triangulations have the
    # exact same sets of divides
    def __eq__(self, other):
        assert ( isinstance(other, Triangulation) )
        return ((self.has_divides(other.ds)) 
            and (other.has_divides(self.ds)))

    def mu(self, i, j):
        if   i >  j: return i - j
        elif i <= j: return j - i

    def L(self, i):
        return [ a for a in inrange(0, i - 1)
            if Divide(a, i) in self.ds ]

    def R(self, i):
        return [ b for b in inrange(i + 1, self.N + 1)
            if Divide(b, i) in self.ds ]

    def p_L(self, i):
        return safemax([ self.mu(i, a) for a in self.L(i) ])

    def p_R(self, i):
        return safemax([ self.mu(i, b) for b in self.R(i) ])

    def w(self, i):
        return self.p_L(i) * self.p_R(i)

    def x(self, i):
        if self.coxeter_graph.is_Down(i):
            return self.w(i)
        else:
            return self.N + 1 - self.w(i)

    # gets the embedded point in R^(N+1)
    # corresponding to this triangulation
    def get_embedded_point(self):
        return [ self.x(i) for i in inrange(1, self.N) ]

    # self has exactly all but
    # exactly 1 Divide in common with other
    def is_i_linked(self, other, i):
        assert ( isinstance(other, Triangulation) )
        count_different = len([ d for d in self.ds if not d in other.ds ])
        return count_different == i


#
### Triangulations Graph
#
# + Creates a network of Triangulations,
#   where two triangulations are linked if
#   they share all but 1 Divide in common
#
class TriangulationGraph:

    def __init__(self, ts):
        assert ( all([isinstance(t, Triangulation)
            for t in ts ]) )

        self.ts = ts
        # create 1-linked graph
        self.links = [ (t1, t2)
            for t1, t2 in it.combinations(self.ts, 2)
            if t1.is_i_linked(t2, 1) ]

    # get all of the triangulations that
    # have all of ds divides
    def get_triangulations_with_divides(self, ds):
        return [ t for t in self.ts
            if t.has_divides(ds) ]
    
    # gets an ordered cycle of
    # the embedded points of K-3
    # (for K-3, the embedded shape will
    # be a 2D pentagon embedded in 3D)
    def get_triangulations_ordered_2D(self):
        assert ( self.ts[0].N == 3 ) # only for K-3

        ts = self.ts[:]
        cycle = []

        # get the first triangulation
        # that is 1-linked with t
        def get_next(t):
            for t_next in ts:
                if t.is_i_linked(t_next, 1):
                    return t_next

        while len(ts) > 0:

            # pick a start
            if len(cycle) == 0:
                cycle.append(ts[0])
                ts.remove(ts[0])
            # pick a triangulation that
            # is 1-linked with the
            # triangulation just added
            else:
                t_next = get_next(cycle[-1])
                cycle.append(t_next)
                ts.remove(t_next)

        return cycle





