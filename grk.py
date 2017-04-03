import indset
import coloring
import tables
import networkx as nx
import math

s_gen = tables.getTableGenerator()

i = 0
for s in s_gen:
    #generate the confusability graph G of X given Y, YR
    gxyyr = indset.generateGXYYR(s)
    
    gxyyr2 = nx.strong_product(gxyyr, gxyyr)
    
    #print "gxyyr2 nodes:"
    #print gxyyr2.nodes()
    
    #print "gxyyr2 edges:"
    #print gxyyr2.edges()
    
    #print "MIS number for gxyyr2: "
    #print indset.setUtil(gxyyr2)
    #from that generate G R given K graphs.
    grk = indset.generateGRK(gxyyr, s)
    
    grk2 = indset.generateGRK2(gxyyr2, s)

    #print "num of grk2 graphs to consider: {}".format(len(grk2))

    r1 = min([coloring.minimalColoring(g1) for g1 in grk])

    if i%100 == 0:
        print "r1 {}".format(r1)

    for g2 in grk2:
        if coloring.minimalColoring(g2) < r1:
            print "Found s matching, s:\n{}\n\ngrk^2:{}".format(s,g2.nodes())
    i+=1
    
