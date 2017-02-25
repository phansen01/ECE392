import networkx as nx
import matplotlib.pyplot as plt
from random import choice

def setUtil(graph):
    if graph.number_of_nodes() == 0:#G is empty
        return 0

    #v = any vertex in G
    v = choice(graph.nodes())
    neighborhood = graph.copy().neighbors(v) + [v]
    #print neighborhood

    withV = graph.copy()
    withV.remove_nodes_from(neighborhood)

    withoutV = graph.copy()
    withoutV.remove_node(v)

    return max(1 + setUtil(withV), setUtil(withoutV)) 

G = nx.cycle_graph(5)
S = nx.strong_product(G, G)
Q = nx.strong_product(G, S)
print setUtil(Q)
