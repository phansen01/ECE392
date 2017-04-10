import networkx as nx
import matplotlib.pyplot as plt
from multiprocessing import Pool
#from functools import partial
import itertools
from random import choice


def colorIsSafe(graph, neighbors, color):
    for n in neighbors:
        if graph.node[n]['color'] == color:
            return False
    return True

def countColorsUsed(graph):
    d = {}
    for n in graph.nodes():
        currentColor = graph.node[n]['color']
        if currentColor not in d:
            d[currentColor] = 1

    return len(d.keys())

def maxCommonColorSet(graph):
    d = {}
    for n in graph.nodes():
        currentColor = graph.node[n]['color']
        if currentColor not in d:
            d[currentColor] = [n]
        else:
            d[currentColor].append(n)

    maxCount = 0
    c = -1
    for color in d.keys():
        if len(d[color]) > maxCount:
            maxCount = len(d[color])
            c = color
    return d[c]


def verifyColoring(graph):
    for n in graph.nodes():
        neighbors = graph.neighbors(n)
        for m in neighbors:
            if graph.node[m]['color'] == graph.node[n]['color']:
                return False
    return True


#k = number of colors, n = current vertex index
def colorUtil(vertex, vertexList, graph, k, n):
    #get the adjacent vertices of this vertex
    neighbors = graph.neighbors(vertex)

    if n == (len(graph) - 1): #we're at the last vertex
        #if this vertex is colorable, we've colored all vertices
        for color in xrange(1, k+1):
            if colorIsSafe(graph, neighbors, color):
                graph.node[vertex]['color'] = color
        #if we weren't able to color this vertex, return false
        if graph.node[vertex]['color'] == -1:
            return False
        return True
        

    for color in xrange(1,k+1):
        if colorIsSafe(graph, neighbors, color):
            #this color is safe, try assigning it
            graph.node[vertex]['color'] = color

            if colorUtil(vertexList[n+1], vertexList, graph, k, n+1):
                return True
            #if this coloring didn't lead to a solution, backtrack
            graph.node[vertex]['color'] = -1

    return False

def colorHelper(g, k):
    if colorUtil(g.nodes()[0], g.nodes(), g, k, 0):
        return True

    return False

def colorHelper_star(a_b):
    """Convert `f([1,2])` to `f(1,2)` call."""
    return colorHelper(*a_b)


def minimalColoringMP(g):
    if len(g.nodes()) == 0:
        return 0

    p = Pool(4)

    max_degree = max([g.degree(v) for v in g.nodes()])

    upper_bound = max_degree + 1

    cliques = list(nx.find_cliques(g))

    if len(cliques) == 0:
        lower_bound = 1

    else:
        lower_bound = len(max(cliques))

    #print "lower bound: {}, upper bound: {}".format(max_clique_size, upper_bound)

    if upper_bound == lower_bound:
        return upper_bound

    for n in g.nodes():
        g.node[n]['color'] = -1

    colorings = range(lower_bound, upper_bound + 1)
    #graphs = [g.copy() for _ in range(len(colorings))]

    #print colorings
    #print graphs

    chi = p.map(colorHelper_star,
                 itertools.izip(
                     itertools.repeat(g.copy()),
                     colorings)
    ).index(True) + 1
    #print "chi = {}".format(chi)
    return chi


def minimalColoring(g, r):

    # max_degree = max([g.degree(v) for v in g.nodes()])

    # upper_bound = max_degree + 1

    #lower bound
    #max_clique_size = len(max(list(nx.find_cliques(g))))    #max_degree = max([g.degree(v) for v in g.nodes()])
    cliques = list(nx.find_cliques(g))
    if len(cliques) == 0:
        lower_bound = 1
    else:
        lower_bound = len(max(cliques))

    #dont bother coloring if lower bound is more than we are
    #looking for
    if lower_bound > r:
        return lower_bound

    for n in g.nodes():
        g.node[n]['color'] = -1
    
    for k in range(lower_bound, len(g.nodes()) + 1):
        #attempt a k-coloring
        if colorUtil(g.nodes()[0], g.nodes(), g, k, 0):
            #print k
            return k

        # if verifyColoring(g):
        #     print k
        #     return k


# g = nx.cycle_graph(6)


# g2 = nx.strong_product(g, g)



#print minimalColoringMP(g2)

# graphs = [nx.dense_gnm_random_graph(choice(range(25,30)), choice(range(15,150))) for _ in range(100)]
# # #print graphs
# #print min([minimalColoring(x) for x in graphs])
# for x in graphs:
#     minimalColoring(x)

# print "colors used:"
# print countColorsUsed(S)
# print "Largest set with same color:"
# print maxCommonColorSet(S)
# print "With size %d" % len(maxCommonColorSet(S))
#print "verify solution: "
#verifyColoring(S)


#drawing
# pos = nx.circular_layout(S)

# colorList = []
# labels = {}
# #matplotlib maps color integers to some range, can control
# #this using a parameter to draw_networkx_nodes apparently
# for n in S.nodes():
#     colorList.append(S.node[n]['color'])
#     labels[n] = n


# nx.draw_networkx_nodes(S, pos,
#                        node_color=colorList,
#                        node_size=620
#                        )
# nx.draw_networkx_edges(S,pos,width=1.0,alpha=0.5)
                       
# nx.draw_networkx_labels(S,pos,labels,font_size=10, font_color='white')

# plt.axis('off')
# plt.savefig("labels_and_colors.png") # save as png
# plt.show() # display


# UB = 25
# LB = 25
# chi = -1
# M = 0

#print chi
# M = number of colors used in current coloring
# LB = lower bound on chi(G)
# UB = upper bound on chi(G)
# def RecursiveColorAssignment(vertex, vertexList, index, graph):
#     global chi
#     global UB
#     global M
#     print vertex
#     neighbors = graph.neighbors(vertex)
#     for color in colors:
#         if colorIsSafe(graph, neighbors, color):
#             graph.node[vertex]['color'] = color
#             break
#     if index == len(graph) - 1: #if we're at the last vertex
#         M = countColorsUsed(graph)
#         if chi < M:
#             chi = M
#             #save the current coloring
#             if M == LB:
#                 return
#             else:
#                 UB = M - 1
#     else:
#         return RecursiveColorAssignment(vertexList[index+1], vertexList, index+1, graph)


