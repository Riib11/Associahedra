# To Do

*Problem*: For K5, the unfolding into 3D isn't working right. I think that there is a problem in how it is choosing a basis for each facet4 (which is a 3D facet that lies in R4).

- *Solution* (Idea): In a separate notebook, try to create a working algorithm for taking a 3D polytope, translating it into 4D in the same way that a facet4 of K5 is embedded in R4, and then recovering it correctly. If I can get this sort of algorithm to work, then I'm sure that I could have it just run seamlessly in `K5_net.nb`as well!
  - result: I did this, but I'm still having problems for how K5 ends up looking. It works for K4, but not K5... this is especially annoying. It HAS to be something happening in the projection, because the stereographically projected result is perfect for the vertices/edges/etc. that I produced via the Python program.

- *Next*: Go through just the first face of K5 and see if I can unfold it satisfactorily. Try different choices for basis. The idea is that, to unfold, each "piece" gets its own orthonormal basis and then is projected into 3D using it. This relies on the assumption that each piece lies on a 3D hyperplane. Which should be the case... the entire K4 lies on a 4D hyperplane, so if the faces are flat, as they are, then they are 3D. The problem point is in transforming those pieces.
