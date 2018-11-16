# To Do

*Problem*: For K5, the unfolding into 3D isn't working right. I think that there is a problem in how it is choosing a basis for each facet4 (which is a 3D facet that lies in R4).

- *Solution* (Idea): In a seperate notebook, try to create a working algorithm for taking a 3D polytope, translating it into 4D in the same way that a facet4 of K5 is embedded in R4, and then recovering it correctly. If I can get this sort of algorithm to work, then I'm sure that I could have it just run seemlessly in `K5_net.nb`as well!