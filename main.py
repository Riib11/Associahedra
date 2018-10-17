from debug import *
from mathematica import *
from Triangulation import Triangulation, TriangulationGraph

from K import K

#
### Parameters
#

N = 3
dim = 1

#
### Constructions
#

k = K(N)
triangulations = k.get_all_triangulations(dim)
triangulations_graph = TriangulationGraph(N, triangulations)

log("1-paritions", triangulations_graph.get_i_partitions(1))

# triangulations_ordered = (
#     triangulations_graph.get_triangulations_ordered_2D())
# embedded_points_ordered = (to_table([tri.get_embedded_point()
#     for tri in triangulations_ordered]))

# log("triangulations (ordered)", triangulations_ordered)
# log("embedded points (ordered)", embedded_points_ordered)