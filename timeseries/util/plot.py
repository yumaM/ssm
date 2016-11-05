#coding: utf-8
import numpy as np
import pandas as pd
#from pandas import Series, DataFrame
from matplotlib import pyplot as plt
import networkx as nx

def sp_matrix(i, j):
    mat = np.random.randn(i,j)
    mat[abs(mat)<1] = 0
    #mat = mat.map(lambda x: 0 if np.abs(x)>0.5 else x)
    return np.matrix(mat)

def heatmap(data, **labels):
    data = np.array(data)
    fig, axis = plt.subplots(figsize=(10, 10))
    heatmap = axis.pcolor(data, cmap=plt.cm.Reds)
    axis.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
    axis.set_yticks(np.arange(data.shape[1])+0.5, minor=False)
    axis.invert_yaxis()
    axis.xaxis.tick_top()
    if labels:
        axis.set_xticklabels(labels["row"], minor=False)
        axis.set_yticklabels(labels["column"], minor=False)
    fig.show()
    #plt.savefig('image.png')
    return heatmap

def digraph(data):
    DG = nx.DiGraph()
    idxs = data.index.tolist()
    #print idxs
    for idx_from in idxs:
        for idx_to in idxs:
            #print idx_from, idx_to
            #print data.loc[idx_from, idx_to]
            if data.ix[idx_from,idx_to]!=0:
                #print B.ix[idx_from,idx_to]
                DG.add_edge(idx_from, idx_to, weight=data.ix[idx_from,idx_to])
    pos = nx.spring_layout(DG)
    nx.draw_networkx_nodes(DG, pos, node_size = 100, node_color = 'w')
    nx.draw_networkx_edges(DG, pos)
    nx.draw_networkx_labels(DG, pos, font_size = 12, font_family = 'sans-serif', font_color = 'r')
    plt.xticks([])
    plt.yticks([])
    plt.show()