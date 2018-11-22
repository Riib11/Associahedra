"""
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+
|  ~>>            Triangulation            <<~  |
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+


"""

from utilities import *
from debug import *
from copy import deepcopy
import itertools as it

from Divide import Divide
from Graph import Graph

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

    @classmethod
    def embed_recursive(cls, x):
        assert ( isinstance(x, list)
            or isinstance(x, Triangulation) )
        if isinstance(x, list):
            return list(map(cls.embed_recursive, x))
        else:
            return x.get_embedded_point()

    # self and other have exactly
    # i Divides in common
    def is_i_linked(self, other, i):
        assert ( isinstance(other, Triangulation) )
        return i <= len([d for d in self.ds if d in other.ds])


#
### Triangulations Graph
#
# + Creates a network of Triangulations,
#   where nodes represent (N - 1)-triangulations
#   on the given polygon (vertices)
#
# + An 'i-facet' is a group of Triangulations
#   in this graph where each of its triangulations
#   is i-linked to each other of its triangulations.
#
# + A 'vertex' is a 0-facet. Note that a vertex
#   is a group that consists of just 1 triangulation.
#
class TriangulationGraph:

    def __init__(self, N, k, ts=None):
        self.N = N
        self.V = N + 2
        self.k = k
        self.ts = ts or k.get_all_triangulations(N - 1)

    # gets a subgraph of this graph
    # with just the given triangulations
    def get_subgraph(self, ts):
        return TriangulationGraph(self.N, self.k, ts)

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
        # set of all possible divides
        ds_all = [ Divide(v1, v2) for v1, v2 in
            it.combinations(inrange(0, self.V - 1), 2) ]

        parts = list( filter(
            lambda ts: len(ts) > 2, # filter
            [ self.get_triangulations_with_divides(ds)
                for ds in it.combinations(ds_all, i) ]))
        # DEBUG
        for ts in parts:
            if len(ts) < 3:
                print("[!] small parts:", ts)
                print()

        return parts

        # iterate through all i-combinations of divides
        # in `ds_all`, each which represent a segement of
        # the parition of the triangulations
        return list( filter(
            lambda ts: len(ts) > 2, # filter
            [ self.get_triangulations_with_divides(ds)
                for ds in it.combinations(ds_all, i) ]))

    # gets the set of ordered facet2s
    # [requires] at least 2D associahedra (K3)
    # [outputs]  [[ Triangulation ]] = [ facet2 ]
    def get_facet2s(self):
        assert ( self.N >= 3 )
        i = (self.N - 1) - 2 # dim = 2
        return [ self.order_facet2(ts)
            for ts in self.get_i_partitions(i) ]

    # given a facet2, orders the vertex
    # triangulations into a single cycle,
    # which is friendly to Mathematica's
    # Polygon function.
    def order_facet2(self, ts):
        i = (self.N - 1) - 1 # dim = 1
        # must be a facet (linked 1 dimension up (i-1))
        assert ( all([ t1.is_i_linked(t2, i - 1)
            for t1, t2 in it.combinations(ts, 2) ]) )

        # DEBUG
        # if len(ts) < 3: raise Exception("small ts:", ts)
        
        ts = deepcopy(ts)
        # get the next triangulation
        # that is i-linked with t
        def get_next(t):
            for t_next in ts:
                if t.is_i_linked(t_next, i):
                    return t_next
        # order all the triangulations
        # into a cycle
        cycle = []
        while len(ts) > 0:
            # first, pick a start
            if len(cycle) == 0:
                cycle.append(ts[0])
                ts.remove(ts[0])
            # subsequently, pick a triangulation that
            # is i-linked with the triangulation just added
            else:
                t_next = get_next(cycle[-1])
                cycle.append(t_next)
                ts.remove(t_next)
        return cycle

    # gets the set of facet3s, each of which
    # is a set of ordered facet2s.
    # [requires] at least 3D associahedra (K4)
    # [outputs] [[[ Triangulation ]]] = [ facet3 ]
    def get_facet3s(self):
        assert ( self.N >= 4 )
        i = (self.N - 1) - 3 # dim = 3
        return [ facet.get_facet2s()
            for facet in [ self.get_subgraph(ts) # facet3s
            for ts in self.get_i_partitions(i) ] ]

    # gets the same set of facet3s as `get_facet3s`
    # but in the form of a graph, in which
    # two facet3s are linked if they share a
    # facet2 in common. Such a link is labeled
    # with the facet2
    # [requires] at least 3D associahedra (K4)
    # [outputs] Graph< [[ Triangulation ]] = facet3 >
    def get_graphed_facet3s(self):
        assert ( self.N >= 4 )
        # TODO