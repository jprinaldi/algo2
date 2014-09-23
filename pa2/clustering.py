#!/usr/bin/env python3

"""
Implementation of an algorithm for computing a max-spacing k-clustering.
"""

import argparse

class Node:
    def __init__(self, key):
        self.key = key
        self.parent = self
        self.rank = 0
    def __hash__(self):
        return self.key
    def __repr__(self):
        return str(self.key)
    def find(self):
        if self != self.parent:
            self.parent = self.parent.find()
        return self.parent
    def __eq__(self, that):
        return self.key == that.key
    def union(self, that):
        self_root = self.find()
        that_root = that.find()
        if self_root == that_root:
            return
        if self.rank < that.rank:
            self_root.parent = that_root
        elif self.rank > that.rank:
            that_root.parent = self_root
        else:
            that_root.parent = self_root
            self.rank += 1

class Edge:
    def __init__(self, node1, node2, cost):
        self.node1 = node1
        self.node2 = node2
        self.cost = cost
    def __lt__(self, that):
        return self.cost < that.cost
    def __repr__(self):
        return "{} {} {}".format(self.node1, self.node2, self.cost)

def read_file(filename):
    with open(filename) as f:
        num_nodes = int(f.readline())
        edges = []
        key_to_node = {}
        for line in f:
            node1_key, node2_key, cost = [int(x) for x in line.split()]
            if node1_key not in key_to_node.keys():
                key_to_node[node1_key] = Node(node1_key)
            if node2_key not in key_to_node.keys():
                key_to_node[node2_key] = Node(node2_key)
            edge = Edge(key_to_node[node1_key], key_to_node[node2_key], cost)
            edges.append(edge)
        edges.sort()
    return key_to_node, edges

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute a max-spacing k-clustering")
    parser.add_argument('filename', type=str, help="file containing graph")
    parser.add_argument('k', type=int, help="target number of clusters")

    args = parser.parse_args()

    key_to_node, edges = read_file(args.filename)
    edge_key = 0
    clusters = len(key_to_node.keys())
    while clusters > args.k:
        edge = edges[edge_key]
        if edge.node1.find() != edge.node2.find():
            edge.node1.union(edge.node2)
            clusters -= 1
        edge_key += 1
    for edge in edges:
        if edge.node1.find() != edge.node2.find():
            print(edge.cost)
            break
