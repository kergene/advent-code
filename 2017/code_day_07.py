#import hashlib

#from math import prod
#from math import ceil
#from math import gcd

#from numpy import base_repr
#import numpy as np

#from sympy.ntheory.modular import crt
#from sympy.ntheory import divisor_sigma

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

#import sys


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = dict(preprocess(datum) for datum in data)
    return data




def preprocess(datum):
    if '->' in datum:
        datum = datum.split(' -> ')
        root, children = datum
        children = children.split(', ')
    else:
        root = datum
        children = []
    root = root.split()
    weight = int(root[1][1:-1])
    root = root[0]
    return root, {'weight': weight, 'children': children}


def part_1(data):
    children = set(program for subdict in data.values() for program in subdict['children'])
    for program in data:
        if program not in children:
            return program


def part_2(base, data):
    weigh_tower(base, data)
    return solution


class Memoize:
    def __init__(self, func):
        self.func = func
        self.memo = {}
    
    def __call__(self, program, data):
        if program not in self.memo:
            self.memo[program] = self.func(program, data)
        return self.memo[program]


@Memoize
def weigh_tower(program, data):
    subdict = data[program]
    children = subdict['children']
    if len(children) == 0:
        return subdict['weight']
    else:
        above_weights = [weigh_tower(child, data) for child in children]
        possibles = set(above_weights)
        if len(possibles) > 1:
            repeated_val = [x for x in possibles if above_weights.count(x) > 1][0]
            possibles.remove(repeated_val)
            non_repeated_val = possibles.pop()
            idx = above_weights.index(non_repeated_val)
            failing_prog = children[idx]
            global solution
            solution = data[failing_prog]['weight'] + repeated_val - non_repeated_val
        else:
            repeated_val = possibles.pop()
        return len(above_weights) * repeated_val + subdict['weight']


def main():
    year, day = 2017, 7
    data = get_data(year, day)
    base = part_1(data)
    print(base)
    print(part_2(base, data))


if __name__ == "__main__":
    main()
