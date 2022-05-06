"""
Label propagation community detection algorithms.
Source: https://networkx.org/documentation/stable/_modules/networkx/algorithms/community/label_propagation.html#label_propagation_communities
"""
from collections import Counter, defaultdict

import networkx as nx
from networkx.utils import groups
from networkx.utils import not_implemented_for
from networkx.utils import py_random_state

__all__ = ["label_propagation_communities"]



def label_propagation_communities(G):
    
    coloring = _color_network(G)
    labeling = {v: k for k, v in enumerate(G)}
    while not _labeling_complete(labeling, G):
        for color, nodes in coloring.items():
            for n in nodes:
                _update_label(n, labeling, G)

    clusters = defaultdict(set)
    for node, label in labeling.items():
        clusters[label].add(node)
    return clusters.values()



def _color_network(G):

    coloring = dict() 
    colors = nx.coloring.greedy_color(G)
    for node, color in colors.items():
        if color in coloring:
            coloring[color].add(node)
        else:
            coloring[color] = {node}
    return coloring


def _labeling_complete(labeling, G):


    return all(
        labeling[v] in _most_frequent_labels(v, labeling, G) for v in G if len(G[v]) > 0
    )


def _most_frequent_labels(node, labeling, G):

    if not G[node]:

        return {labeling[node]}

    freqs = Counter(labeling[q] for q in G[node])
    max_freq = max(freqs.values())
    return {label for label, freq in freqs.items() if freq == max_freq}


def _update_label(node, labeling, G):

    high_labels = _most_frequent_labels(node, labeling, G)
    if len(high_labels) == 1:
        labeling[node] = high_labels.pop()
    elif len(high_labels) > 1:
        # Prec-Max
        if labeling[node] not in high_labels:
            labeling[node] = max(high_labels)