class Graph:
    def __init__(self):
        self.nodes = []
        self.links = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_link(self, node1, node2, label):
        self.links.append((node1, node2, label))

    def get_links_to(self, node):
        for (n1, n2, label) in self.links:
            if node in [n1, n2]:
                yield (n1, n2, label)