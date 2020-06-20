class DegreeView():
    def __init__(self, G, weight=None):
        self._graph = G
        self._succ =  G._adj
        self._pred =  G._adj
        self._nodes = self._succ 
        self._weight = weight

    def __iter__(self):
        weight = self._weight
        if weight is None:
            for n in self._nodes:
                succs = self._succ[n]
                preds = self._pred[n]
                yield (n, len(succs) + len(preds))
        else:
            for n in self._nodes:
                succs = self._succ[n]
                preds = self._pred[n]
                deg = sum(dd.get(weight, 1) for dd in succs.values()) \
                    + sum(dd.get(weight, 1) for dd in preds.values())
                yield (n, deg)

def core_number(G):
    degrees = dict(G.degree())
    nodes = sorted(degrees, key=degrees.get)
    bin_boundaries = [0]
    curr_degree = 0
    for i, v in enumerate(nodes):
        if degrees[v] > curr_degree:
            bin_boundaries.extend([i] * (degrees[v] - curr_degree))
            curr_degree = degrees[v]
    node_pos = {v: pos for pos, v in enumerate(nodes)}
    core = degrees
    nbrs = {v: list(all_neighbors(G, v)) for v in G.nodes()}
    for v in nodes:
        for u in nbrs[v]:
            if core[u] > core[v]:
                nbrs[u].remove(v)
                pos = node_pos[u]
                bin_start = bin_boundaries[core[u]]
                node_pos[u] = bin_start
                node_pos[nodes[bin_start]] = pos
                nodes[bin_start], nodes[pos] = nodes[pos], nodes[bin_start]
                bin_boundaries[core[u]] += 1
                core[u] -= 1
    return core

def all_neighbors(graph, node):
    values = graph.neighbors(node)
    return values

def neighbors(G, n):
    """Returns a list of nodes connected to node n. """
    return G.neighbors(n)
        
class Graph():
    node_attr_dict_factory = dict
    adjlist_dict_factory = dict
    edge_attr_dict_factory = dict

    def __init__(self):
        self.node_attr_dict_factory = self.node_attr_dict_factory
        self.adjlist_dict_factory = self.adjlist_dict_factory
        self.edge_attr_dict_factory = self.edge_attr_dict_factory

        self._node = self.node_attr_dict_factory()  
        self._adj = self.adjlist_dict_factory()  

    def add_edge(self, u_of_edge, v_of_edge):
        u, v = u_of_edge, v_of_edge
        if u not in self._node:
            self._adj[u] = self.adjlist_dict_factory()
            self._node[u] = self.node_attr_dict_factory()
        if v not in self._node:
            self._adj[v] = self.adjlist_dict_factory()
            self._node[v] = self.node_attr_dict_factory()
        data = self._adj[u].get(v, self.edge_attr_dict_factory())
        self._adj[u][v] = data
        self._adj[v][u] = data

    def degree(self):
        return DegreeView(self)

    def neighbors(self, n):
        return iter(self._adj[n])

    def nodes(self):
        nodes = NodeView(self)
        return nodes

class NodeView():
    def __init__(self, graph):
        self._nodes = graph._node

    def __len__(self):
        return len(self._nodes)

    def __iter__(self):
        return iter(self._nodes)

    def __getitem__(self, n):
        return self._nodes[n]