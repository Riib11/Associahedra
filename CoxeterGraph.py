#
### Coxeter Graph
#
class CoxeterGraph:
    def __init__(self, N):
        self.N = N
        # yields the most simple orientation
        self.edges = [ (i, i + 1) for i in inrange(1, N - 1) ]
        # set of Ups and Downs
        self.U = [ i for i in inrange(N) if self.is_Up(i) ]
        self.D = [ i for i in inrange(N) if self.is_Down(i) ]

    def is_Up(self, i):
        return not self.is_Down(i)

    def is_Down(self, i):
        if i in [1, self.N]:
            return True
        else:
            return (i - 1, i) in self.edges