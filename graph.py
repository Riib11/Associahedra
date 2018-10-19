"""
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+
|  ~>>                Graph                <<~  |
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+

A simple, undirected graph that supports
labeled links, where the labels can be any object.

"""

class Graph:
    def __init__(self):
        self.nodes = []
        self.links = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_link(self, node1, node2, label):
        # add any nodes not already added
        [ nodes.append(n) for n in [node1, node2]
            if not n in self.nodes ]
        self.links.append((node1, node2, label))

    # get all links that
    # touch the given node
    # [note] generator
    def get_links_to(self, node):
        assert ( node in self.nodes )
        for (n1, n2, label) in self.links:
            if node in [n1, n2]:
                yield (n1, n2, label)