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

from collections import defaultdict
#from collections import Counter

from heapdict import heapdict

#from queue import SimpleQueue
#from queue import LifoQueue
#from queue import Empty

#from itertools import product
from itertools import combinations
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
    datum = datum.split('; ')
    valve = datum[0].split(' ')
    tunnels = datum[1].split(', ')
    current_valve = valve[1]
    rate = int(valve[-1].split('=')[1])
    tunnels = set(tunnel[-2:] for tunnel in tunnels)
    return current_valve, rate, tunnels


def prep_dijkstra(data):
    valve_flows = {}
    valve_paths = {}
    for valve, rate, tunnels in data:
        valve_flows[valve] = rate
        valve_paths[valve] = tunnels
    all_paths = defaultdict(set)
    for valve, flow in valve_flows.items():
        # never will be at 0 flow valve except AA
        if flow != 0 or valve == 'AA':
            seens = {}
            heap = heapdict()
            heap[valve] = 0
            while heap:
                choice, distance = heap.popitem()
                seens[choice] = distance
                new_dist = distance + 1
                for tunnel in valve_paths[choice]:
                    if tunnel not in seens:
                        if tunnel not in heap or heap[tunnel] > new_dist:
                            heap[tunnel] = new_dist
            for new_valve, dist in seens.items():
                # never will go to 0 flow valve
                if valve_flows[new_valve] != 0 and valve != new_valve:
                    all_paths[valve].add((new_valve, dist))
    return all_paths, valve_flows


def part_1(data):
    # we assume AA has flow rate 0
    all_paths, valve_flows = prep_dijkstra(data)
    # try to run dijkstra's using location, open_list, score: minutes
    best_scores = run_dijkstras(all_paths, valve_flows, 0)
    return max(best_scores.values())


def part_2_old(data):
    # originally did it like this, where I iterated over all pairs of outputs
    # but this is slow
    # we assume AA has flow rate 0
    all_paths, valve_flows = prep_dijkstra(data)
    # try to run dijkstra's using location, open_list, score: minutes
    best_scores = run_dijkstras(all_paths, valve_flows, 4)
    best_total = max(best_scores.values())
    print('Individual best: ', best_total)
    print('Possibilities: ', len(best_scores), len(best_scores) ** 2)
    for human, elephant in combinations(best_scores.keys(), 2):
        if all(x < 2 for x in sum_tuples(human, elephant)):
            score = best_scores[human] + best_scores[elephant]
            if best_total < score:
                best_total = score
    return best_total


def run_dijkstras(all_paths, valve_flows, start_time, opens=None):
    location = 'AA'
    counter = 0
    valve_index = {}
    for valve in all_paths.keys():
        if valve != 'AA':
            valve_index[valve] = counter
            counter += 1
    if opens is None:
        opens = tuple([0] * (len(all_paths.keys()) - 1))
    pressure_seens = set()
    pressure_heap = heapdict()
    # start at start_time minutes
    pressure_heap[location, opens, 0] = start_time
    best_scores = defaultdict(int)
    while pressure_heap:
        # we check when time >= 29 or all valves open
        # use 29 as can't do anything in last minute
        key, minutes = pressure_heap.popitem()
        pressure_seens.add(key)
        location, opens, score = key
        # can open valve if not at AA and valve is closed
        if location != 'AA' and opens[valve_index[location]] == 0:
            new_opens = list(opens)
            new_opens[valve_index[location]] = 1
            new_opens = tuple(new_opens)
            new_minutes = minutes + 1
            new_score = score + valve_flows[location] * (30 - new_minutes)
            new_key = location, new_opens, new_score
            if best_scores[new_opens] < new_score:
                best_scores[new_opens] = new_score
            # move on if done
            if all(new_opens) or minutes >= 29:
                pass
            elif new_key not in pressure_seens:
                if new_key not in pressure_heap or pressure_heap[new_key] > new_minutes:
                    pressure_heap[new_key] = new_minutes
        # check movement to other valves
        for target_valve, extra_time in all_paths[location]:
            new_minutes = minutes + extra_time
            # only move if target valve is closed and won't take 30 mins already
            if new_minutes < 29 and opens[valve_index[target_valve]] == 0:
                new_location = target_valve
                new_key = new_location, opens, score
                if new_key not in pressure_seens:
                    if new_key not in pressure_heap or pressure_heap[new_key] > new_minutes:
                        pressure_heap[new_key] = new_minutes
    return best_scores


def part_2(data):
    # we assume AA has flow rate 0
    all_paths, valve_flows = prep_dijkstra(data)
    # try to run dijkstra's using location, open_list, score: minutes
    best_scores = run_dijkstras(all_paths, valve_flows, 4)
    best_single = max(best_scores.values())
    # rerun dijkstra's on outut
    best_total = best_single
    for opens, score in sorted(best_scores.items(), key=lambda x: x[1], reverse=True):
        if score + best_single < best_total:
            return best_total
        additional_bests = run_dijkstras(all_paths, valve_flows, 4, opens=opens)
        test_score = score + max(additional_bests.values())
        if best_total < test_score:
            best_total = test_score
    return best_total


def sum_tuples(tuple1, tuple2):
    return tuple(sum(pair) for pair in zip(tuple1, tuple2))


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
