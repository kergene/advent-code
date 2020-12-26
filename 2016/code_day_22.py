import numpy as np
from itertools import product
import sys


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = dict(preprocess(datum) for datum in data[2:])
    return data


def preprocess(datum): # pos Size Used Avail
    datum = datum.split()
    pos = datum[0].split('-')[-2:]
    pos = tuple(int(i[1:]) for i in pos)
    used = int(datum[2][:-1])
    avail = int(datum[3][:-1])
    total = int(datum[1][:-1])
    return pos, {'used':used, 'avail':avail, 'total':total}


def visualise(data):
    large_width = 400
    np.set_printoptions(linewidth=large_width, threshold=sys.maxsize)
    grid = np.zeros((30, 35), np.int16)
    for i in range(30):
        for j in range(35):
            if data[(i, j)]['used'] == 0:
                zero = (i, j)
            grid[i][j] = data[(i, j)]['used']
    print(grid)
    print(zero, 'is empty')


def viable_pairs(data):
    viables = 0
    for i, j in product(data, repeat=2):
        if data[i]['used'] != 0 and data[j]['avail'] >= data[i]['used']:
            viables += 1
    return viables


def manhattan_distance(a, b):
    x_a, y_a = a
    x_b, y_b = b
    return abs(x_a - x_b) + abs(y_a - y_b)


def fewest_moves(data):
    # general solution is 'prohibitavely expensive' (creator)
    # hand counting a solution here is the fastest way
    # this solution deals with the specific case at hand
    # note from printed grid we can only move one square
    zero = (4, 25)
    target = (29, 0)
    gap = (0, 16)
    me = (0, 0)
    # move zero to gap
    moves_to_gap = manhattan_distance(zero, gap)
    # move in the sensible path (target data put in (28, 0))
    moves_to_target = manhattan_distance(gap, target)
    moved_target = (28, 0)
    # move target to top
    # takes 5 moves of zero to move target by 1 in straight line
    moves_to_me = manhattan_distance(moved_target, me) * 5
    return moves_to_gap + moves_to_target + moves_to_me


def move_data(start, end, data):
    data[end]['used'] += data[start]['used']
    data[end]['avail'] -= data[start]['used']
    data[start]['avail'] += data[start]['used']
    data[start]['used'] = 0
    return data


def main():
    year, day = 2016, 22
    data = get_data(year, day)
    visualise(data)
    print(viable_pairs(data))
    print(fewest_moves(data))


if __name__ == "__main__":
    main()
