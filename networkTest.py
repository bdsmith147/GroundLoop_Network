# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 01:56:42 2019

@author: benjamin
"""


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import itertools as it
names = np.loadtxt("Lab Components.csv", delimiter=',', usecols=0, dtype=str)
graph_name = names[0]
names = names[1:]
#print(names)

G = nx.Graph()
G.add_nodes_from(names)



connections = np.loadtxt("Connections.csv", delimiter=',', dtype=str)
connections = connections[1:, 1:]
edge_list = []
for i, row in enumerate(connections):
    z = it.zip_longest([names[i]], names[np.where(connections[i] =='x')[0]], 
                       fillvalue=names[i])
    edge_list.append([i for i in z])
edge_list = list(it.chain(*edge_list))
#print(edge_list)
G.add_edges_from(edge_list, color='k', weight=1)
#G.remove_nodes_from(['NI 1', "NI 3"])
#G.remove_edge('RF Switch', 'RF Amp')

fig = plt.figure(figsize=(5,5)) 
ax = fig.add_subplot()
#ax.set_aspect('equal')
d = nx.coloring.greedy_color(G, strategy='largest_first')
nx.draw_circular(G, with_labels=True, ax=ax)
cycles = nx.algorithms.cycles.cycle_basis(G, 'GND')
for cyc in cycles: 
    cyc.append(cyc[0])
gcycles = list(np.array(cycles)[['GND' in cycles[i] for i in range(len(cycles))]])
gcycles = list(np.array(gcycles)[['RF P. Supply' in gcycles[i] for i in range(len(gcycles))]])
cycles = gcycles
cNum = 0

cyc_edges = [tuple((cycles[cNum][i], cycles[cNum][i+1])) for i in range(len(cycles[cNum])-1)]

H = nx.Graph()
H.add_nodes_from(G)
G.add_edges_from(cyc_edges, color='b', weight=4)
edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]
weight = [G[u][v]['weight'] for u,v in edges]
pos = nx.circular_layout(G)
nx.draw(G, pos, edges=edges, with_labels=True, ax=ax, edge_color=colors, width=weight)
