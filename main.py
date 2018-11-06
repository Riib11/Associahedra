from debug import *
from utilities import *
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
triangulations_graph = TriangulationGraph(N, k)
facets = triangulations_graph.get_facet3s()

embedded_facet = Triangulation.embed_recursive(facets)
log("embedded facets", to_table( embedded_facet ))