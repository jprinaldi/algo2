#!/usr/bin/env python3

"""
Implementation of Prim's algorithm for computing a minimum spanning tree of a graph.
"""

import argparse
import heapq
import random

class Adjacency:
    def __init__(self, node, weight):
        self.node = node
        self.weight = weight
    def __lt__(self, that):
        return self.weight < that.weight
    def __repr__(self):
        return str(self.node)+" "+str(self.weight)

class Graph:
    def __init__(self, num_nodes = None, num_edges = None):
        self.num_nodes = num_nodes
        self.num_edges = num_edges
        self.nodes = set()
        self.adjacencies = {}
    def add_node(self, node):
        if node in self.nodes:
            return
        self.nodes.add(node)
        self.adjacencies[node] = set()
    def add_adjacency(self, node, adjacency):
        self.adjacencies[node].add(adjacency)

def create_graph(filename):
    edges = set()
    with open(filename) as f:
        num_nodes, num_edges = [int(x) for x in next(f).split()]
        g = Graph(num_nodes, num_edges)
        for line in f:
            node1, node2, weight = [int(x) for x in line.split()]
            adjacency1 = Adjacency(node2, weight)
            adjacency2 = Adjacency(node1, weight)
            g.add_node(node1)
            g.add_node(node2)
            g.add_adjacency(node1, adjacency1)
            g.add_adjacency(node2, adjacency2)
    return g

def prim(graph):
    visited_nodes = set()
    node = random.sample(graph.nodes, 1)[0]
    visited_nodes.add(node)
    candidate_adjacencies = []
    for new_adjacency in graph.adjacencies[node]:
        heapq.heappush(candidate_adjacencies, new_adjacency)
    tree_weight = 0
    while visited_nodes != graph.nodes:
        adjacency = heapq.heappop(candidate_adjacencies)
        while adjacency.node in visited_nodes:
            adjacency = heapq.heappop(candidate_adjacencies)
        visited_nodes.add(adjacency.node)
        tree_weight += adjacency.weight
        for new_adjacency in graph.adjacencies[adjacency.node]:
            if new_adjacency.node not in visited_nodes:
                heapq.heappush(candidate_adjacencies, new_adjacency)
    return tree_weight

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute a minimum spanning tree of a graph")
    parser.add_argument('filename', type=str, help="file containing graph")
    
    args = parser.parse_args()

    g = create_graph(args.filename)
    print(prim(g))