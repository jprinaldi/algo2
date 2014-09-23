#!/usr/bin/env python3

"""
Implementation of a dynamic programming algorithm
for solving the Travelling Salesman Problem (TSP).
"""

import argparse
import copy
import itertools
import math

INFINITY = float('inf')

class City:
    def __init__(self, key, x, y):
        self.key = key
        self.x = x
        self.y = y
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)
    def distance(self, that):
        return math.sqrt((self.x - that.x)**2 + (self.y - that.y)**2)

def read_file(filename):
    with open(filename) as f:
        num_cities = int(f.readline())
        cities = {}
        key = 1
        for line in f:
            x, y = [float(s) for s in line.split()]
            city = City(key, x, y)
            cities[key] = city
            key += 1
    return num_cities, cities

def get_subsets(S, m):
    return itertools.combinations(S, m)

def get_index(S):
    return sum([2**key for key in S if key != 1]) << 3

def tsp(n, cities):
    global verbose
    new = {1: 0}

    for m in range(2, n + 1):
        if verbose: print("Solving for", m, "cities...")

        old = copy.copy(new)
        new = {}

        for S in get_subsets(cities.keys(), m):
            if 1 not in S: continue
            for j in S:
                if j == 1: continue
                index = get_index(S)
                new[index + j] = min([old[index - 2**(j + 3) + k] + cities[k].distance(cities[j])
                                     if index - 2**(j + 3) + k in old.keys()
                                     else INFINITY
                                     for k in S
                                     if k != j])

    index = get_index(cities.keys())
    best_value = min([new[index + j] + cities[j].distance(cities[1]) for j in range(2, n + 1)])
    return best_value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve the Travelling Salesman Problem")
    parser.add_argument('filename', type=str, help="file containing cities")
    parser.add_argument('--verbose', action='store_true', help="print additional messages")

    args = parser.parse_args()
    
    num_cities, cities = read_file(args.filename)
    verbose = args.verbose
    min_cost_tour = tsp(num_cities, cities)
    print(min_cost_tour)
