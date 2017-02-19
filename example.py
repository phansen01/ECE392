import networkx as nx

#basic example
G = nx.cycle_graph(5)
A1 = nx.nx_agraph.to_agraph(G)
A1.draw('testpentagon', format='png', prog='circo')
strong = nx.strong_product(G,G)
A2 = nx.nx_agraph.to_agraph(strong)
A2.draw('teststrong', format='png', prog='circo')

print nx.maximum_independent_set(strong)
