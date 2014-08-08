#!/usr/bin/env python3

"""
Implementation of top-down and bottom-up dynamic programming algorithms
for solving the 0/1 Knapsack Problem.
"""

import argparse
import sys

class Item:
    def __init__(self, key, value, weight):
        self.key = key
        self.value = value
        self.weight = weight
    def __hash__(self):
        return self.key
    def __repr__(self):
        return str(self.value) + " " + str(self.weight)

def read_data(filename):
    with open(filename) as f:
        knapsack_size, number_of_items = [int(x) for x in f.readline().split()]
        items = {}
        key = 0
        for line in f:
            value, weight = [int(x) for x in line.split()]
            item = Item(key, value, weight)
            items[key] = item
            key += 1
    return knapsack_size, number_of_items, items

class Knapsack:
    def __init__(self, knapsack_size, number_of_items, items):
        self.knapsack_size = knapsack_size
        self.number_of_items = number_of_items
        self.items = items
        self.m = {}
    def top_down_solve(self, size, item_key):
        sys.setrecursionlimit(10000)

        if item_key <= 0:
            return 0
        
        if item_key in self.m.keys() and size in self.m[item_key].keys():
            return self.m[item_key][size]

        if item_key not in self.m.keys():
            self.m[item_key] = {}
        item = self.items[item_key]

        if item.weight > size:
            self.m[item_key][size] = self.top_down_solve(size, item_key - 1)
        else:
            self.m[item_key][size] = max(self.top_down_solve(size, item_key - 1),
                                         self.top_down_solve(size - item.weight, item_key - 1) + item.value)

        return self.m[item_key][size]
        
    def bottom_up_solve(self):
        global verbose
        self.m[0] = {}
        for x in range(self.knapsack_size + 1):
            self.m[0][x] = 0
        for size in range(self.knapsack_size + 1):
            if verbose:
                if size % 1000 == 0: print("Solving for size =", size, "...")
            for item_key in range(1, self.number_of_items):
                item = self.items[item_key]
                if item_key not in self.m.keys():
                    self.m[item_key] = {}
                if item.weight > size:
                    self.m[item_key][size] = self.m[item_key - 1][size]
                else:
                    self.m[item_key][size] = max(self.m[item_key - 1][size],
                                                 self.m[item_key - 1][size - item.weight] + item.value)
        return self.m[self.number_of_items - 1][self.knapsack_size]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve the 0/1 Knapsack Problem")
    parser.add_argument('filename', type=str, help="file containing items")
    parser.add_argument('algorithm', metavar="algorithm", type=int, choices=range(0, 2), help="0: top-down, 1: bottom-up")
    parser.add_argument('--verbose', action='store_true', help="print additional messages")

    args = parser.parse_args()

    verbose = args.verbose
    knapsack_size, number_of_items, items = read_data(args.filename)
    k = Knapsack(knapsack_size, number_of_items, items)
    if args.algorithm == 0:
        solution = k.top_down_solve(knapsack_size, number_of_items - 1)
    elif args.algorithm == 1:
        solution = k.bottom_up_solve()
    print(solution)