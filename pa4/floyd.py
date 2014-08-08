#!/usr/bin/env python3

"""
Implementation of the Floyd-Warshall algorithm
for solving the all-pairs shortest-path problem.
"""

import argparse

INFINITY = float('inf')

class Edge:
    def __init__(self, tail, length):
        self.tail = tail
        self.length = length

def read_file(filename):
    with open(filename) as f:
        num_vertices, num_edges = [int(x) for x in f.readline().split()]
        tail_to_head = {}
        for vertex in range(1, num_vertices + 1):
            tail_to_head[vertex] = {}
        for line in f:
            tail, head, length = [int(x) for x in line.split()]
            tail_to_head[tail][head] = length
    return num_vertices, num_edges, tail_to_head

def floyd_warshall(n, tail_to_head):
    global verbose
    a = {}
    shortest_path_length = INFINITY

    for i in range(1, n + 1):
        a[i] = {}
        for j in range(1, n + 1):
            if i == j:
                a[i][j] = 0
            elif j in tail_to_head[i].keys():
                a[i][j] = tail_to_head[i][j]
            else:
                a[i][j] = INFINITY
    
    for k in range(1, n):
        if verbose: print("Iteration:", k)
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                a[i][j] = min(a[i][j], a[i][k] + a[k][j])

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            a[i][j] = min(a[i][j], a[i][n] + a[n][j])
            if a[i][j] < shortest_path_length:
                shortest_path_length = a[i][j]
    
    # Check for negative cycles by inspecting diagonal
    for i in range(1, n + 1):
        if a[i][i] < 0:
            return None
    
    return shortest_path_length

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve the all-pairs shortest-path problem")
    parser.add_argument('filename', type=str, help="file containing graph")
    parser.add_argument('--verbose', action='store_true', help="print additional messages")

    args = parser.parse_args()
    
    verbose = args.verbose
    num_vertices, num_edges, tail_to_head = read_file(args.filename)
    print(floyd_warshall(num_vertices, tail_to_head))