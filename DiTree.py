import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

class DiTree:
    _seed = 42
    _rng = np.random.default_rng(_seed)
    G = nx.DiGraph()
    W = nx.to_numpy_array(G)

    def __init__(self):
        return

    # G_R graph
    def __random_root_tree(self, n, m):
        actual_m = np.clip(m, n-1, n*(n-1)) # clip m to be within range of possible number of edges
        G = nx.DiGraph()
        # root node
        G.add_node(0)
        for i in range(1, n):
            parent_node = self._rng.choice(list(G.nodes))
            G.add_node(i)
            G.add_edge(parent_node, i)
        i = 0
        actual_m -= (n-1)
        while i < actual_m:
            v_a, v_b = tuple(self._rng.choice(n, size=2, replace=False))   # prevent self-edges
            if not G.has_edge(v_a, v_b):
                G.add_edge(v_a, v_b)
                i += 1
        return G

    # G_C graph
    def __random_sink_tree(self, n, m):
        actual_m = np.clip(m, n-1, n*(n-1)) # clip m to be within range of possible number of edges
        G = nx.DiGraph()
        # sink node
        G.add_node(0)
        for i in range(1, n):
            child_node = self._rng.choice(list(G.nodes))
            G.add_node(i)
            G.add_edge(i, child_node)
        i = 0
        actual_m -= (n-1)
        while i < actual_m:
            v_a, v_b = tuple(self._rng.choice(n, size=2, replace=False))   # prevent self-edges
            if not G.has_edge(v_a, v_b):
                G.add_edge(v_a, v_b)
                i += 1
        return G
    
    def __assign_weights(self, G: nx.DiGraph, is_row_stoch: bool):
        A = nx.to_numpy_array(self.G)
        W = np.zeros((A.shape))
        if is_row_stoch:
            max_degree = max([val for (_, val) in G.in_degree()])
            alpha = 1 / max_degree
            for i in G.nodes:
                in_neighbors = list(G.predecessors(i))
                num_in_neighbors = len(in_neighbors)
                for j in in_neighbors:
                    W[i][j] = alpha
                W[i,i] = 1 - (num_in_neighbors * alpha)
        else:
            max_degree = max([val for (_, val) in G.out_degree()])
            alpha = 1 / max_degree
            for i in G.nodes:
                out_neighbors = list(G.successors(i))
                num_out_neighbors = len(out_neighbors)
                for j in out_neighbors:
                    W[j][i] = alpha
                W[i,i] = 1 - (num_out_neighbors * alpha)
        return W

    def sparse_tree_digraph(self, n, m, is_row_stoch=True):
        self.G = self.__random_root_tree(n, m) if is_row_stoch else self.__random_sink_tree(n, m)
        self.W = self.__assign_weights(self.G, is_row_stoch)
        return self.G, self.W

    def get_stoch_matrix(self):
        return self.W

def is_row_stochastic(A: np.ndarray):
    _, n = A.shape
    print(f"Sum of rows: {A.sum(1)}")
    return np.equal(np.round(A.sum(1)), np.ones(n)).all() # must round to handle floating point error

def is_col_stochastic(A: np.ndarray):
    m, _ = A.shape
    print(f"Sum of columns: {A.sum(0)}")
    return np.equal(np.round(A.sum(0)), np.ones(m)).all()

def draw_dir_graph(G: nx.DiGraph):
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos=pos)
    plt.show()