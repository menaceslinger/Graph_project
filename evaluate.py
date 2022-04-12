import networkx as nx
import numpy as np
import pandas as pd
from itertools import combinations


def avg_internal_density(graph, clustering):
    aid = []
    list_clustering=list(clustering)
    coms = [tuple(x) for x in list_clustering]
    for comz in coms:
        community = graph.subgraph(comz)
        mx = len(community.edges())
        nx = len(community.nodes())
        try:
            internal_density = float(mx) / (float(nx * (nx - 1)) / 2)
            aid.append(internal_density)
        except:
            return 0
    return np.mean(aid)

def cut_ratio(g, clustering):
    cutr = []
    list_clustering=list(clustering)
    comzz = [tuple(x) for x in list_clustering]
    for como in comzz:
        coms = g.subgraph(como)
        ns = len(coms.nodes())
        edges_outside = 0
        for n in coms.nodes():
            neighbors = g.neighbors(n)
            for n1 in neighbors:
                if n1 not in coms:
                    edges_outside += 1
        try:
            ratio = float(edges_outside) / (ns * (len(g.nodes()) - ns))
            cutr.append(ratio)
        except:
            return 0
        return ratio
    return np.mean(cutr)



def cov_per(G, partition):

    node_community = {}
    for i, community in enumerate(partition):
        for node in community:
            node_community[node] = i

    if not G.is_multigraph():
        possible_inter_community_edges = sum(
            len(p1) * len(p2) for p1, p2 in combinations(partition, 2)
        )

        if G.is_directed():
            possible_inter_community_edges *= 2
    else:
        possible_inter_community_edges = 0

    n = len(G)
    total_pairs = n * (n - 1)
    if not G.is_directed():
        total_pairs //= 2

    intra_community_edges = 0
    inter_community_non_edges = possible_inter_community_edges

    for e in G.edges():
        if node_community[e[0]] == node_community[e[1]]:
            intra_community_edges += 1
        else:
            inter_community_non_edges -= 1

    coverage = intra_community_edges / len(G.edges)

    if G.is_multigraph():
        performance = -1.0
    else:
        performance = (intra_community_edges + inter_community_non_edges) / total_pairs

    return coverage, performance