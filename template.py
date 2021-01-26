#import hashlib

#from math import prod
#from math import ceil
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

#import sys


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data




def preprocess(datum):
    return datum




def part_1(data):
    return




def part_2(data):
    return




def main():
    year, day = 2017, 0
    data = get_data(year, day)
    print(data)
    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
