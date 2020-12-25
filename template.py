#import hashlib

#from math import prod
#from math import ceil

#from numpy import base_repr
#import numpy as np

#from sympy.ntheory.modular import crt
#from sympy.ntheory import divisor_sigma

#import re

#from collections import defaultdict
#from collections import Counter

#from itertools import product
#from itertools import combinations
#from itertools import permutations

#from copy import deepcopy

#import sys


def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
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
    day = 0
    data = get_data(day)
    print(data)
    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
