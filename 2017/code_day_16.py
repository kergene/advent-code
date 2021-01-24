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

from time import perf_counter_ns


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(',')
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return [datum[0]] + datum[1:].split('/')


def dance(data):
    program_length = 16
    array = [chr(x + 97) for x in range(program_length)]
    array = run_loop(array, data)
    return ''.join(array)


def run_loop(array, data):
    for line in data:
        if line[0] == 's':
            spin = int(line[1])
            array = array[-spin:] + array[:-spin]
        elif line[0] == 'x':
            idx_1 = int(line[1])
            idx_2 = int(line[2])
            array[idx_1], array[idx_2] = array[idx_2], array[idx_1]
        elif line[0] == 'p':
            idx_1 = array.index(line[1])
            idx_2 = array.index(line[2])
            array[idx_1], array[idx_2] = array[idx_2], array[idx_1]
        else:
            assert False, line[0]
    return array


def fast_forward(data):
    program_length = 16
    array = [chr(x + 97) for x in range(program_length)]
    seens = set()
    while True:
        rep = ''.join(array)
        if rep in seens:
            break
        else:
            seens.add(rep)
        array = run_loop(array, data)
    loop_len = len(seens)
    remainder = (10 ** 9) % loop_len
    array = [chr(x + 97) for x in range(program_length)]
    for _ in range(remainder):
        array = run_loop(array, data)
    return ''.join(array)


def main():
    year, day = 2017, 16
    data = get_data(year, day)
    print(dance(data))
    print(fast_forward(data))


if __name__ == "__main__":
    main()
