from debug import *
from utilities import *
from mathematica import *
from Triangulation import Triangulation, TriangulationGraph

from K import K

#
### Parameters
#

N = 5

#
### Constructions
#

k = K(N)
triangulations_graph = TriangulationGraph(N, k)
facets = triangulations_graph.get_3facets()

embedded_facet = Triangulation.embed_recursive(facets)
log("embedded facet", to_table( embedded_facet ))