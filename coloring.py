import networkx as nx



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
                print 'false'
    print 'true'


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

            if colorUtil(vertexList[n+1], vertexList, graph, k, n+1) == True:
                return True
            #if this coloring didn't lead to a solution, backtrack
            graph.node[vertex]['color'] = -1

    return False

#test out algorithm
G = nx.cycle_graph(5)
S = nx.strong_product(G,G)

for n in S.nodes():
    S.node[n]['color'] = -1

for n in G.nodes():
    G.node[n]['color'] = -1

vertexIter = nx.nodes_iter(S)
vertexList = []

for v in vertexIter:
    vertexList.append(v)

#attempt a 5 coloring
colorUtil(vertexList[0], vertexList, S, 5, 0)

for n in S.nodes(data=True):
    print n
print "colors used:"
print countColorsUsed(S)
print "Largest set with same color:"
print maxCommonColorSet(S)
print "verify solution: "
verifyColoring(S)



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


