"""
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+
|  ~>>               Polygon               <<~  |
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+


"""

from utilities import *
from debug import *
import itertools as it

from Divide import Divide
from Triangulation import Triangulation

#
### Polygon
#
class Polygon:
    def __init__(self, N, coxeter_graph):
        self.N = N
        self.V = N + 2

        # label vertices according to
        # Coxeter graph
        self.coxeter_graph = coxeter_graph
        self.vertices = []
        self.vertices.append(0)
        for x in self.coxeter_graph.D:
            self.vertices.append(x)
        self.vertices.append(self.N + 1)
        for x in reversed(self.coxeter_graph.U):
            self.vertices.append(x)

        # init divide index function
        # get_divide_index : Divide -> Index
        self.get_divide_index = (
            Divide.get_divide_index_func(self.V))

    # the minimum number of vertices, 
    # along the permimeter of the polygon,
    # between two vertices
    def get_perimeter_distance(self, d):
        assert ( isinstance(d, Divide) )

        dist1 = abs(d.v1 - d.v2) % self.V
        dist2 = abs(d.v1 - d.v2 + self.V) % self.V
        dist = min(dist1, dist2)

        assert ( dist >= 0 )
        return dist

    def get_vertex_between(self, v1, v2): pass

    # is this divide just a part of
    # the polygon's perimeter?
    # note: each side includes the divide's vertices
    def is_on_perimeter(self, d):
        assert ( isinstance(d, Divide) )
        return self.get_perimeter_distance(d) == 1

    # partition the polygon's vertices
    # into two sets, divided along
    # the given divide
    # note: the divide's vertices are
    #       in each set
    def get_partitioned_vertices(self, d):
        assert ( isinstance(d, Divide) )

        side1 = [d.v1, d.v2]
        v = (d.v1 + 1) % self.V
        while v != d.v2:
            side1.append(v)
            v = (v + 1) % self.V

        side2 = [d.v1, d.v2]
        v = (d.v1 - 1) % self.V
        while v != d.v2:
            side2.append(v)
            v = (v - 1) % self.V

        return side1, side2

    # will the addition of the new
    # divide `d_new` be valid given the
    # existent divide `d`?
    def is_valid_new_divide(self, d, d_new):
        assert ( isinstance(d, Divide)
            and isinstance(d_new, Divide) )

        side1, side2 = self.get_partitioned_vertices(d)
        non_intersecting = (d_new.is_contained_in_vertices(side1)
            or d_new.is_contained_in_vertices(side2))
        distinct = d != d_new

        # if non_intersecting and distinct and d == Divide(1,4) and d_new == Divide(0,3):
        #     log("valid divide", str(d)+", "+str(d_new))
        #     log("sides", str(side1)+", "+str(side2))

        return non_intersecting and distinct


    # does this collection of divides
    # yield a valid triangulation?
    def is_valid_triangulation(self, ds):
        assert ( all([isinstance(d, Divide) for d in ds]) )
        return all([ self.is_valid_new_divide(d1, d2)
            for d1, d2 in it.combinations(ds, 2)])

    # generate all the triangulations that
    # use `self.N - dim` divides
    def get_all_triangulations(self, dim):
        divides_count = self.N - dim

        if divides_count < 0: return []
        if divides_count == 0:
            return [ Triangulation(self.N, [], self,
                self.coxeter_graph, self.get_divide_index) ]

        all_divides = [ Divide(d1, d2)
            for d1, d2 in it.combinations(inrange(0, self.V - 1), 2)
            if not self.is_on_perimeter(Divide(d1, d2)) ]

        # log("all_divides", all_divides)

        # proto-triangulations
        prototris = [ [d] for d in all_divides ]
        for _ in range(divides_count-1):
            prototris_new = []
            for tri in prototris:
                for d in all_divides:
                    tri_new = tri[:] + [d]
                    if self.is_valid_triangulation(tri_new):
                        prototris_new.append(tri_new)
            prototris = prototris_new

        # log("prototris:", prototris)

        # convert to Triangulation type
        # and remove duplicates
        triangulations = []
        for ds in prototris:
            tri = Triangulation(self.N, ds, self,
                self.coxeter_graph, self.get_divide_index)
            if tri not in triangulations: # uses custom equality
                triangulations.append(tri)

        return triangulations
