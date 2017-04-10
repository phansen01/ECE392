import indset
import coloring
import tables
import networkx as nx
import math
import time

s_gen = tables.getTableGenerator()

i = 0
start = time.time()
for s in s_gen:
    
    #known to be a working example
    if i <= 99141633:
        i+=1
        continue
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
    pairs = indset.generateGRK(gxyyr, s)
    # grklist = [grk for (grk, k) in pairs]
    # klist = [k for (grk, k) in pairs]

    r1 = 4
    g1min = nx.Graph()
    k1min = []
    for (g1, k1) in pairs:
        c = coloring.minimalColoring(g1, 0)
        
        if c < r1:
            r1 = c
            g1min = g1.copy()
            k1min = k1
        
    if r1 == 1:
        i+=1
        continue

    pairs2 = indset.generateGRK2(gxyyr2, s)

    
    r2 = 10 #needs to be set to some junk value > number of nodes in g2
    g2min = nx.Graph()
    k2min = []
    for (g2, k2) in pairs2:
        c = coloring.minimalColoring(g2,r1)
        
        if c < r2:
            r2 = c
            g2min = g2.copy()
            k2min = k2

    if math.sqrt(float(r2)) < r1:
        print "i = {}\nnumber of colors for r2: {}".format(i,r2)
        print "Found s matching, s:\n{}\n\ngrk^2:{}".format(s,g2min.nodes())
        print "grk^2 edges: {}".format(g2min.edges())
        print "grk^1 edges: {}".format(g1min.edges())
        print "gxyyr^1 edges: {}".format(gxyyr.edges())
        print "gxyyr^2 edges: {}".format(gxyyr2.edges())
        print "MIS for grk^1: {}\nMIS for grk^2: {}".format(k1min, k2min)
        break

    if i%100 == 0:
        end = time.time()
        print "i={}, time per 100: {}".format(i,end - start)
        start = time.time()
        print "r1 = {}".format(r1)
        print "r2 = {}".format(r2)



    i+=1
    
