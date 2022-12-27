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
#     def __call__(self, state, data):
#         if state not in self.memo:
#             self.memo[state] = self.func(state, data)
#         return self.memo[state]
#
#     def clear(self):
#         self.memo.clear()

#sign = lambda x: (x > 0) - (x < 0)


def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data




def preprocess(datum):
    return datum




def part_1(data):
    total = 0
    for idx, row in enumerate(data):
        pass
    return total




def part_2(data):
    total = 0
    for idx, row in enumerate(data):
        pass
    return total




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
