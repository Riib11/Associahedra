#
### Triangulation
#
class Triangulation:
    def __init__(self, N, ds, polygon, coxeter_graph, 
        get_divide_index # Divide -> Index
    ):
        assert ( polygon.is_valid_triangulation(ds) )

        self.N = N
        self.ds = sorted(ds, key=get_divide_index)
        self.polygon = polygon
        self.coxeter_graph = coxeter_graph

    def tostring(self): return "Tri"+str(self.ds)
    __str__ = tostring
    __repr__ = tostring

    def issubset(self, other):
        assert ( isinstance(other, Triangulation) )
        return all([ d in other.ds for d in self.ds ])

    def __eq__(self, other):
        assert ( isinstance(other, Triangulation) )
        return (self.issubset(other)) and (other.issubset(self))

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

    def get_embedded_point(self):
        return [ self.x(i) for i in inrange(1, self.N) ]