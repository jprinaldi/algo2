#!/usr/bin/env python3

"""
Implementation of an algorithm for computing a max-spacing k-clustering.
Assumes distances are defined implicitly
as the Hamming distance between two nodes' labels.
"""

import argparse
import copy

class Node:
    def __init__(self, key, label):
        self.parent = self
        self.rank = 0
        self.label = label
        self.key = key
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
    def hd(self, that):
        zipped = zip(self.label, that.label)
        z = [1 if x != y else 0 for (x, y) in zipped]
        return sum(z)
    def get_close_labels(self):
        close_labels = set()
        for i in range(24):
            new_label = copy.copy(self.label)
            new_label[i] = 1 - new_label[i]
            close_labels.add(b2d(new_label))
        for i in range(23):
            for j in range(i+1, 24):
                new_label = copy.copy(self.label)
                new_label[i] = 1 - new_label[i]
                new_label[j] = 1 - new_label[j]
                close_labels.add(b2d(new_label))
        return close_labels

class Edge:
    def __init__(self, node1, node2, cost):
        self.node1 = node1
        self.node2 = node2
        self.cost = cost
    def __lt__(self, that):
        return self.cost < that.cost
    def __repr__(self):
        return str(self.node1) + " " + str(self.node2) + " " + str(self.cost)
    
def b2d(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out

def read_file(filename):
    with open(filename) as f:
        num_nodes, label_size = [int(x) for x in f.readline().split()]
        key_to_node = {}
        for line in f:
            label = [int(x) for x in line.split()]
            key = b2d(label)
            node = Node(key, label)
            key_to_node[key] = node
    return num_nodes, key_to_node

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute a max-spacing k-clustering")
    parser.add_argument('filename', type=str, help="file containing graph")
    parser.add_argument('--verbose', action='store_true', help="print additional messages")

    args = parser.parse_args()

    num_nodes, key_to_node = read_file(args.filename)
    it = 0

    for node in key_to_node.values():
        if args.verbose:
            it += 1
            if it % 1000 == 0: print("Iteration:", it)
        close_labels = node.get_close_labels()
        for key in close_labels:
            if key in key_to_node.keys():
                node.union(key_to_node[key])
    
    reps = set()

    for node in key_to_node.values():
        reps.add(node.find().key)

    print(len(reps))
