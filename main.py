from K import K

#####
####
### Parameters
##
#
N = 3
dim = 1

#####
####
### Constructions
##
#

k = K(N)
triangulations = K.get_all_triangulations(dim)

debug.log("triangulations", triangulations)
debug.log("len = ", len(triangulations))
debug.log("embedded points", to_table([tri.get_embedded_point()
    for tri in triangulations]))