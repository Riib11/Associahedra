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
        self.V = N + 2
        self.ds = sorted(ds, key=get_divide_index)
        self.polygon = polygon
        self.coxeter_graph = coxeter_graph

    def tostring(self): return "T"+str(self.ds)
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

    # self and other have exactly
    # i Divides in common
    def is_i_linked(self, other, i):
        assert ( isinstance(other, Triangulation) )
        return i <= len([d for d in self.ds if d in other.ds])


#
### Triangulations Graph
#
# + Creates a network of Triangulations,
#   where nodes represent i-triangulations
#   on the given polygon
#
class TriangulationGraph:

    def __init__(self, N, k, dimension):
        self.N = N
        self.V = N + 2
        self.k = k
        self.ts = k.get_all_triangulations(N - 1 - dimension)

    # get all of the triangulations that
    # have all of ds divides
    def get_triangulations_with_divides(self, ds):
        return [ t for t in self.ts
            if t.has_divides(ds) ]

    # get list of groups of triangulations,
    # where each group is of triangulations
    # is such that each member is i-linked
    # with every other member.
    # each group is a (N - 1 - i)-dimensional facet of K
    def get_i_partitions(self, i):
        ds_all = [] # [Divide]
        for t in self.ts:
            for d in t.ds:
                if not d in ds_all: ds_all.append(d)

        ds_all = [ Divide(v1, v2) for v1, v2 in
            it.combinations(inrange(0, self.V - 1), 2) ]

        # iterate through all i-sized combinations
        # in `ds_all`, each which represent a segement of
        # the parition of the triangulations
        return list(filter(lambda ts: ts != [],
            [ self.get_triangulations_with_divides(ds)
            for ds in it.combinations(ds_all, i) ]))

    # gets a set of 2D 'facets', each of which
    # is a cycle of Triangulations, ordered to make
    # the perimeter of the facet
    # [requires] at least 2D associahedra
    def get_ordered_facets2D(self):
        assert ( self.N >= 3 )
        i = (self.N - 1) - 2 # dim = 2
        return [ self.order_facet2D(ts)
            for ts in self.get_i_partitions(i) ]

    # given a 2D facet, orders the 'vertex'
    # triangulations into a single cycle,
    # which is friendly to Mathematica's
    # Polygon function.
    def order_facet2D(self, ts):
        i = (self.N - 1) - 1 # dim = 1
        # must be a facet (linked 1 dimension up (i-1))
        assert ( all([ t1.is_i_linked(t2, i - 1)
            for t1, t2 in it.combinations(ts, 2) ]) )
        
        ts = ts[:]
        log("ts before ordering", ts)
        # get the first triangulation
        # that is 1-linked with t
        def get_next(t):
            for t_next in ts:
                if t.is_i_linked(t_next, i):
                    return t_next
        # order all the triangulations
        # into a cycle
        cycle = []
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
        log("ts after ordering", cycle)
        return cycle

    # gets a set of 3D facets, each of which
    # is a set of 2D facets. Each 2D facet is
    # a cycle of Triangulations, ordered to
    # make the perimeter of the 2D facet
    # [requires] at least 3D associahedra
    def get_facets3D(self):
        assert ( self.N >= 4 )
        i = (self.N - 1) - 2 # dim = 
        return [ self.order_facet2D(ts)
            for ts in self.get_i_partitions(i) ]

    # gets the same set of 3D facets as `get_facets3D`
    # but in the form of a graph, in which
    # two 3D facets are linked if they share a
    # 2D facet in common. Such a link is labeled
    # with the 2D facet
    # [requires] at least 3D associahedra
    def get_graphed_facets3D(self):
        assert ( self.N >= 4 )
        # TODo