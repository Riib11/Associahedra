from debug import *
from mathematica import *
from Triangulation import Triangulation, TriangulationGraph

from K import K

#
### Parameters
#

N = 4

#
### Constructions
#

k = K(N)
triangulations_graph = TriangulationGraph(N, k, dim=0)
# triangulations = k.get_all_triangulations(3)
# log("embedded vertices", to_table(
#     [ t.get_embedded_point() for t in triangulations ]))

faces2D_ordered = triangulations_graph.get_ordered_facets2D()
log("facets 2D (ordered)", faces2D_ordered)
log("embedded faces 2D", to_table([
    [ t.get_embedded_point() for t in ts ]
    for ts in faces2D_ordered ]))