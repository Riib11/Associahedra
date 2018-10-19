
class A:
    value = 1
    __enter__ = lambda self: self
    __exit__ = lambda self, x2, x3, x4: self

with A() as a: print(a.value)