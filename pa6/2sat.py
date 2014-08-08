#!/usr/bin/env python3

"""
Implementation of an algorithm for solving the 2-SAT problem.
"""

import argparse

class Vertex:
    def __init__(self, value):
        self.value = value
    def __eq__(self, that):
        return self.value == that.value
    def __hash__(self):
        return self.value

class Graph:
    def __init__(self):
        self.n = 0
        self.vertices = set()
        self.tail_to_head = {}
        self.head_to_tail = {}
    def add_vertex(self, vertex):
        self.vertices.add(vertex)
        self.tail_to_head[vertex] = set()
        self.head_to_tail[vertex] = set()
        self.n += 1
    def reverse(self):
        temp = self.tail_to_head
        self.tail_to_head = self.head_to_tail
        self.head_to_tail = temp
    def parse_edge_list(self, edge_list):
        for tail, head in edge_list:
            if tail not in self.vertices:
                self.add_vertex(tail)
            if head not in self.vertices:
                self.add_vertex(head)
            self.tail_to_head[tail].add(head)
            self.head_to_tail[head].add(tail)

class Kosaraju:
    def __init__(self, g):
        self.g = g
        self.t = 0
        self.s = None
        self.f = [None for i in range(self.g.n)]
        self.leader_to_vertices = {}
    def first_dfs(self, vertex):
        stack = []
        stack.append(vertex)
        self.visited[vertex] = 1
        while len(stack) > 0:
            n = stack.pop()
            if self.visited[n] == 1:
                stack.append(n)
                self.visited[n] = 2
                for head in g.tail_to_head[n]:
                    if head not in self.visited.keys():
                        self.visited[head] = 1
                        stack.append(head)
            else:
                self.t += 1
                self.f[self.g.n - self.t] = n
    def second_dfs(self, vertex):
        stack = []
        stack.append(vertex)
        while len(stack) > 0:
            vertex = stack.pop()
            self.visited.add(vertex)
            if self.s not in self.leader_to_vertices.keys():
                self.leader_to_vertices[self.s] = set()
            self.leader_to_vertices[self.s].add(vertex)
            for head in g.tail_to_head[vertex]:
                if head not in self.visited:
                    stack.append(head)
    def first_loop(self):
        self.visited = {}
        vertices = list(self.g.vertices)
        vertices.sort(reverse=True)
        for vertex in vertices:
            if vertex not in self.visited:
                self.first_dfs(vertex)
    def second_loop(self):
        self.visited = set()
        for vertex in self.f:
            if vertex not in self.visited:
                self.s = vertex
                self.second_dfs(vertex)
    def run(self):
        self.g.reverse()
        self.first_loop()
        self.g.reverse()
        self.second_loop()
    def show_sccs(self, k):
        sizes = []
        for vertices in self.leader_to_vertices.values():
            sizes.append(len(vertices))
        sizes.sort(reverse=True)
        print(sizes[:k])
    def check(self):
        for component in self.leader_to_vertices.values():
            for vertex in component:
                if -vertex in component:
                    return False
        return True

def parse_data(filename):
    with open(filename) as f:
        n = int(next(f))
        edges = []
        s = set()
        for line in f:
            x, y = [int(i) for i in line.split()]
            edge1 = [-x, y]
            edge2 = [-y, x]
            edges.append(edge1)
            edges.append(edge2)
    return edges

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('filename', type=str, help="file containing edges")
    
    args = parser.parse_args()

    edges = parse_data(args.filename)
    g = Graph()
    g.parse_edge_list(edges)
    k = Kosaraju(g)
    k.run()
    print(k.check())