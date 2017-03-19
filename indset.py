import networkx as nx
#import matplotlib.pyplot as plt
import itertools
from random import choice


#todo: see if there is a speed difference
#between constructing a set of the neighbors and the nodes
#then computing the intersection vs just using
#list comprehension on the lists themselves.
def isIndependent(graph, nodeSet):
    #print nodeSet
    for n in nodeSet:
        if len(set(graph.neighbors(n)) & nodeSet) != 0:
            return False

    return True

def setUtil(graph):
    if graph.number_of_nodes() == 0:#G is empty
        return 0

    v_zero_degree = [v for v in graph.nodes() if graph.degree(v) == 0]
    #G has a vertex degree 0
    if len(v_zero_degree) != 0:
        withoutV = graph.copy()
        withoutV.remove_node(choice(v_zero_degree))
        return 1 + setUtil(withoutV)

    v_one_degree = [v for v in graph.nodes() if graph.degree(v) == 1]
    #G has a vertex degree one
    if len(v_one_degree) != 0:
        v = choice(v_one_degree)
        w = graph.copy().neighbors(v)[0]
        w_neighborhood = graph.neighbors(w) + [w]
        withW = graph.copy()
        withW.remove_nodes_from(w_neighborhood)
        
        v_neighborhood = graph.neighbors(v) + [v]
        withV = graph.copy()
        withV.remove_nodes_from(v_neighborhood)

        return max(1 + setUtil(withV), 1 + setUtil(withW))
        

    v_three_or_more_degree = [v for v in graph.nodes() if graph.degree(v) > 2]
    #G has a vertex degree >=3
    if len(v_three_or_more_degree) != 0:
        v = choice(v_three_or_more_degree)
        neighborhood = graph.neighbors(v) + [v]

        withV = graph.copy()
        withV.remove_nodes_from(neighborhood)

        withoutV = graph.copy()
        withoutV.remove_node(v)

        return max(1 + setUtil(withV), setUtil(withoutV)) 

    #every vertex in G has degree 2
    else:
        v = choice(graph.nodes())
        #should be exactly two of these
        u,w = graph.copy().neighbors(v)
        u_neighborhood = graph.neighbors(u) + [u]
        v_neighborhood = graph.neighbors(v) + [v]
        w_neighborhood = graph.neighbors(w) + [w]
        
        withU = graph.copy()
        withU.remove_nodes_from(u_neighborhood)
        
        withV = graph.copy()
        withV.remove_nodes_from(v_neighborhood)


        withW = graph.copy()
        withW.remove_nodes_from(w_neighborhood)

        return max(1+setUtil(withU), 1+setUtil(withV), 1+setUtil(withW))

G = nx.cycle_graph(7)
S = nx.strong_product(G, G)

# a = nx.convert.to_dict_of_lists(G)

# print [r for r in a]

for n in itertools.combinations(S.nodes(), setUtil(S)):
    if isIndependent(S,set(n)):
        print n



#for s in c:
#    print isIndependent(G, s)

# G2 = nx.cycle_graph(7)
# S2 = nx.strong_product(G2, G2)



#print setUtil(S2)
