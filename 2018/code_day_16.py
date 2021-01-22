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

'''
673 too hi for P1
618 answer for P1
'''
def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split('\n\n\n\n')
    samples, program = data
    samples = samples.split('\n\n')
    samples = [preprocess_sample(sample) for sample in samples]
    program = program.splitlines()
    program = [preprocess_program(line) for line in program]

    return samples, program


def preprocess_sample(sample):
    sample = sample.splitlines()
    before = eval(sample[0].split(': ')[1])
    instruction = [int(i) for i in sample[1].split()]
    after = eval(sample[2].split(': ')[1])
    return (before, instruction, after)


def preprocess_program(line):
    return [int(i) for i in line.split()]


def addr(a, b, c, before):
    after = before.copy()
    after[c] = before[a] + before[b]
    return after


def addi(a, b, c, before):
    after = before.copy()
    after[c] = before[a] + b
    return after


def mulr(a, b, c, before):
    after = before.copy()
    after[c] = before[a] * before[b]
    return after


def muli(a, b, c, before):
    after = before.copy()
    after[c] = before[a] * b
    return after


def banr(a, b, c, before):
    after = before.copy()
    after[c] = before[a] & before[b]
    return after


def bani(a, b, c, before):
    after = before.copy()
    after[c] = before[a] & b
    return after


def borr(a, b, c, before):
    after = before.copy()
    after[c] = before[a] | before[b]
    return after


def bori(a, b, c, before):
    after = before.copy()
    after[c] = before[a] | b
    return after


def setr(a, b, c, before):
    after = before.copy()
    after[c] = before[a]
    return after


def seti(a, b, c, before):
    after = before.copy()
    after[c] = a
    return after


def gtir(a, b, c, before):
    after = before.copy()
    after[c] = int(a > before[b])
    return after


def gtri(a, b, c, before):
    after = before.copy()
    after[c] = int(before[a] > b)
    return after


def gtrr(a, b, c, before):
    after = before.copy()
    after[c] = int(before[a] > before[b])
    return after


def eqir(a, b, c, before):
    after = before.copy()
    after[c] = int(a == before[b])
    return after


def eqri(a, b, c, before):
    after = before.copy()
    after[c] = int(before[a] == b)
    return after


def eqrr(a, b, c, before):
    after = before.copy()
    after[c] = int(before[a] == before[b])
    return after


def find_threes(samples):
    opcodes = [
        addr, addi,
        mulr, muli,
        banr, bani,
        borr, bori,
        setr, seti,
        gtir, gtri, gtrr,
        eqir, eqri, eqrr
    ]
    counter = 0
    for before, instruction, after in samples:
        _, a, b, c = instruction
        matches = [after == func(a, b, c, before) for func in opcodes]
        if sum(matches) >= 3:
            counter += 1
    return counter


def run_program(samples, program):
    opcodes = [
        addr, addi,
        mulr, muli,
        banr, bani,
        borr, bori,
        setr, seti,
        gtir, gtri, gtrr,
        eqir, eqri, eqrr
    ]
    opcode_funcs = [0] * 16
    while any(thing == 0 for thing in opcode_funcs):
        for before, instruction, after in samples:
            opcode, a, b, c = instruction
            matches = [after == func(a, b, c, before) for func in opcodes]
            if sum(matches) == 1:
                opcode_funcs[opcode] = opcodes.pop(matches.index(1))
    register = [0, 0, 0, 0]
    for opcode, a, b, c in program:
        register = opcode_funcs[opcode](a, b, c, register)
    return register[0]


def main():
    year, day = 2018, 16
    samples, program = get_data(year, day)
    print(find_threes(samples))
    print(run_program(samples, program))


if __name__ == "__main__":
    main()
