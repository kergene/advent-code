import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import import_data

#import hashlib

#from math import prod
#from math import ceil
#from math import floor
#from math import gcd

#from numpy import base_repr
#import numpy as np

#from sympy.ntheory.modular import crt
#from sympy.ntheory import divisor_sigma
#from sympy import isprime

#import re

#from collections import defaultdict
#from collections import Counter

#from heapdict import heapdict

#from queue import SimpleQueue
#from queue import LifoQueue
#from queue import Empty

#from itertools import product
#from itertools import combinations
#from itertools import permutations
#from itertools import accumulate
#from itertools import count

#from copy import deepcopy

# from functools import cmp_to_key

# class Memoize:
#     def __init__(self, func):
#         self.func = func
#         self.memo = {}
#
#     def __call__(self, state):
#         if state not in self.memo:
#             self.memo[state] = self.func(state)
#         return self.memo[state]

#sign = lambda x: (x > 0) - (x < 0)


def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data




def preprocess(datum):
    return int(datum)


# 6951 too high???

class DoublyLinkedLoop:
    def __init__(self, iterable):
        self.nodes = []
        self.focus = None
        self.zero = None
        self.len = 0
        for val in iterable:
            self.add(val)
            self.len += 1

    def add(self, val):
        if self.focus is None:
            new_node = DoublyLinkedNode(None, None, val)
        else:
            new_node = DoublyLinkedNode(self.focus, self.focus.next, val)
            new_node.next.prev = new_node
            new_node.prev.next = new_node
        self.focus = new_node
        self.nodes.append(new_node)
        if val == 0:
            self.zero = new_node

    def mix(self):
        for node in self.nodes:
            if node.val > 0:
                for _ in range(node.val % (self.len - 1)):
                    self.swap(node, node.next)
            if node.val < 0:
                for _ in range(abs(node.val) % (self.len - 1)):
                    self.swap(node.prev, node)

    def swap(self, prev_node, next_node):
        # this only swaps the two nodes values
        # need neighbours values too
        # try again
        next_node.next.prev = prev_node
        prev_node.prev.next = next_node
        prev_node.next = next_node.next
        next_node.prev = prev_node.prev
        prev_node.prev = next_node
        next_node.next = prev_node
    
    def score(self):
        assert self.zero is not None
        self.focus = self.zero
        total =  0
        for _ in range(3):
            for _ in range(1000):
                self.focus = self.focus.next
            total += self.focus.val
        return total
    
    def print(self, node):
        start = node
        vals = []
        vals.append(start.val)
        node = start.next
        while start != node:
            vals.append(node.val)
            node = node.next
        print('For:', vals)

    def print_r(self, node):
        start = node
        vals = []
        vals.append(start.val)
        node = start.prev
        while start != node:
            vals.append(node.val)
            node = node.prev
        print('Rev:', vals)


class DoublyLinkedNode:
    def __init__(self, prev_node, next_node, val):
        if prev_node is not None:
            self.prev = prev_node
        else:
            self.prev = self
        if next_node is not None:
            self.next = next_node
        else:
            self.next = self
        self.val = val




def part_1(data):
    dll = DoublyLinkedLoop(data)
    dll.mix()
    return dll.score()




def part_2(data):
    key = 811589153
    data = [val * key for val in data]
    dll = DoublyLinkedLoop(data)
    for _ in range(10):
        dll.mix()
    return dll.score()





def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(data)
    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
