import networkx as nx
#import matplotlib.pyplot as plt
import itertools
from random import choice

#expects a vertex yr, table s, MIS k
def reachableYR(yr, s, k):
    len_y = len(s[0])
    for x in k:
        for y in range(len_y):
            if s[x][y][yr] > 0:
                return True
    return False

def reachableY(y, s, k):
    len_yr = len(s[0][0])
    for x in k:
        for yr in range(len_yr):
            if s[x][y][yr] > 0:
                return True
    return False

def connectGRKEdges(grk, s, k):
    len_x = len(s)
    len_y = len(s[0])
    len_yr = len(s[0][0])

    reachable_yr = grk.nodes()


    #major candidate for refactoring obviously - the huge compound if
    #statement is just checking all of the conditions specified
    #for GR|K
    for y in range(len_y):
        for yr_i in range(len_yr):
            for x_i in range(len_x):
                for yr_j in range(len_yr):
                    for x_j in range(len_x):
                        if (    x_i != x_j
                            and yr_i != yr_j
                            and reachableY(y, s, k)
                            and yr_i in reachable_yr
                            and yr_j in reachable_yr
                            and x_i in k
                            and x_j in k
                            and s[x_i][y][yr_i] > 0
                            and s[x_j][y][yr_j] > 0
                        ):
                            grk.add_edge(yr_i, yr_j)

#generate the confusability graph
def generateGXYYR(s):
    len_x = len(s)
    len_y = len(s[0])
    len_yr = len(s[0][0])

    #initialize nodes of g as x values
    g = nx.Graph()
    g.add_nodes_from([v for v in range(len_x)])

    print "g nodes"
    print g.nodes()

    #todo: can probably refactor this into a
    #list comprehension, not a big deal right now.
    #for each x, check if it is confusable with another x'
    #by exhaustively checking for a common, nonzero (y,yr) pair.
    #add an edge between these two x vertices.
    for x_i in range(len_x):
        for y in range(len_y):
            for yr in range(len_yr):
                for x_j in range(len_x):
                    if (x_i != x_j) and (s[x_i][y][yr] > 0) and (s[x_j][y][yr] > 0):
                        g.add_edge(x_i,x_j)
    
    print "edges after comparison"
    print g.edges()
    return g

#expects G_X|Y,Y_r, s
def generateGRK(g, s):
    len_x = len(s)
    len_y = len(s[0])
    len_yr = len(s[0][0])
    #enumerate all maximum independent sets
    ind = []
    for n in itertools.combinations(g.nodes(), setUtil(g)):
        if isIndependent(g,set(n)):
            ind.append(n)
    print "All MISs of Gx|y,yr:"
    print ind

    for k in ind:
        grk = nx.Graph()
        nodes = [yr for yr in range(len_yr) if reachableYR(yr, s, k)]
        grk.add_nodes_from(nodes)
        print "grk nodes:"
        print grk.nodes()
        connectGRKEdges(grk, s, k)
        print "connected edges in GR|K:"
        print grk.edges()

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


#s indexed as s[x][y][y_r] representing
#p(y = a, y_r = b | x = c)

#this populates s randomly
#s = [[[choice([0,1]) for x in range(5)] for y in range(5)] for z in range(5)]

#this populates s with all zeros so we can assign specific nonzero values...
s = [[[0 for x in range(5)] for y in range(5)] for z in range(5)]

#using the table from the paper plus junk (nonzero) values.
s[0][0][2] = .4
s[0][0][3] = .4
s[0][1][0] = .1
s[0][1][1] = .9
s[1][1][1] = .9
s[1][2][2] = .9
s[2][2][0] = .9
s[2][3][2] = .9
s[3][1][3] = .9
s[3][3][3] = .9
s[3][4][2] = .9
s[4][0][0] = .9
s[4][4][4] = .9

for row in s:
    print row


#generate the confusability graph G of X given Y, YR
gxyyr = generateGXYYR(s)

#from that generate G R given K graphs.
generateGRK(gxyyr, s)


#G = nx.cycle_graph(7)
#S = nx.strong_product(G, G)

# a = nx.convert.to_dict_of_lists(G)

# print [r for r in a]

# for n in itertools.combinations(S.nodes(), setUtil(S)):
#     if isIndependent(S,set(n)):
#         print n



#for s in c:
#    print isIndependent(G, s)

# G2 = nx.cycle_graph(7)
# S2 = nx.strong_product(G2, G2)



#print setUtil(S2)
