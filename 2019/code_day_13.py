#import hashlib

#from math import prod
#from math import ceil

#from numpy import base_repr
#import numpy as np

#from sympy.ntheory.modular import crt
#from sympy.ntheory import divisor_sigma

#import re

from collections import defaultdict
#from collections import Counter

#from itertools import product
#from itertools import combinations
#from itertools import permutations

#from copy import deepcopy

#import sys


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(',')
    data = [int(datum) for datum in data]
    return data


class IntCode:
    def __init__(self, lines, game=0):
        # the game parameter is part of this game
        self.lines = lines.copy()
        self.index = 0
        self.relative_base = 0
        self.input = []
        self.input_index = 0
        self.game = game

    @property
    def len(self):
        return len(self.lines)

    def extend(self, diff):
        self.lines += [0] * (diff + 1)

    def get_val(self, index, parameter):
        if index < 0:
            assert False, 'Index < 0'
        if index >= self.len:
            self.extend(index - self.len)
        if parameter == '2':
            # relative mode
            read_index = self.relative_base + self.lines[index]
            if read_index >= self.len:
                self.extend(read_index - self.len)
            return self.lines[read_index]
        elif parameter == '1':
            # immediate mode
            return self.lines[index]
        elif parameter == '0':
            # position mode
            read_index = self.lines[index]
            if read_index >= self.len:
                self.extend(read_index - self.len)
            return self.lines[read_index]
        else:
            assert False, parameter

    def set_val(self, index, parameter, value):
        if index < 0:
            assert False, 'Index < 0'
        if index >= self.len:
            self.extend(index - self.len)
        if parameter == '2':
            # relative mode
            read_index = self.relative_base + self.lines[index]
            if read_index >= self.len:
                self.extend(read_index - self.len)
            self.lines[read_index] = value
        elif parameter == '1':
            # immediate mode
            self.lines[index] = value
        elif parameter == '0':
            # position mode
            read_index = self.lines[index]
            if read_index >= self.len:
                self.extend(read_index - self.len)
            self.lines[read_index] = value
        else:
            assert False, parameter

    def run_intcode(self, *p_in):
        self.input += list(p_in)
        while True:
            opcode = str(self.lines[self.index])
            instruction = int(opcode[-2:])
            params = opcode[:-2]
            if instruction == 99:
                break
            elif instruction == 1:
                param_length = 3
                params = params.zfill(param_length)
                self.set_val(self.index + 3,
                             params[-3],
                             self.get_val(self.index + 1, params[-1]) + self.get_val(self.index + 2, params[-2]))
                self.index += param_length + 1
            elif instruction == 2:
                param_length = 3
                params = params.zfill(param_length)
                self.set_val(self.index + 3,
                             params[-3],
                             self.get_val(self.index + 1, params[-1]) * self.get_val(self.index + 2, params[-2]))
                self.index += param_length + 1
            elif instruction == 3:
                param_length = 1
                params = params.zfill(param_length)
                # these next two lines are part of this game
                if self.input_index >= len(self.input):
                    self.input.append(self.game.move_towards_ball())
                self.set_val(self.index + 1, params[-1], self.input[self.input_index])
                self.input_index += 1
                self.index += param_length + 1
            elif instruction == 4:
                param_length = 1
                params = params.zfill(param_length)
                output = self.get_val(self.index + 1, params[-1])
                self.index += param_length + 1
                return 0, output
            elif instruction == 5:
                param_length = 2
                params = params.zfill(param_length)
                if self.get_val(self.index + 1, params[-1]):
                    self.index = self.get_val(self.index + 2, params[-2])
                else:
                    self.index += param_length + 1
            elif instruction == 6:
                param_length = 2
                params = params.zfill(param_length)
                if not self.get_val(self.index + 1, params[-1]):
                    self.index = self.get_val(self.index + 2, params[-2])
                else:
                    self.index += param_length + 1
            elif instruction == 7:
                param_length = 3
                params = params.zfill(param_length)
                if self.get_val(self.index + 1, params[-1]) < self.get_val(self.index + 2, params[-2]):
                    self.set_val(self.index + 3, params[-3], 1)
                else:
                    self.set_val(self.index + 3, params[-3], 0)
                self.index += param_length + 1
            elif instruction == 8:
                param_length = 3
                params = params.zfill(param_length)
                if self.get_val(self.index + 1, params[-1]) == self.get_val(self.index + 2, params[-2]):
                    self.set_val(self.index + 3, params[-3], 1)
                else:
                    self.set_val(self.index + 3, params[-3], 0)
                self.index += param_length + 1
            elif instruction == 9:
                param_length = 1
                params = params.zfill(param_length)
                self.relative_base += self.get_val(self.index + 1, params[-1])
                self.index += param_length + 1
            else:
                assert False, instruction
        return 1, 0


def start_game(data):
    game = IntCode(data)
    tiles = defaultdict(int)
    while True:
        exit_code, x = game.run_intcode()
        if exit_code:
            break
        exit_code, y = game.run_intcode()
        if exit_code:
            assert False
        exit_code, tile = game.run_intcode()
        if exit_code:
            assert False
        tiles[(x, y)] = tile
    return sum(tile == 2 for tile in tiles.values())


class Game:
    def __init__(self, data):
        self.machine = IntCode(data, self)
        self.machine.set_val(0, '1', 2)
        self.tiles = defaultdict(int)

    def play_game(self):
        loop = 0
        while True:
            if loop:
                exit_code, x = self.machine.run_intcode()
            else:
                exit_code, x = self.machine.run_intcode()
            if exit_code:
                break
            exit_code, y = self.machine.run_intcode()
            if exit_code:
                assert False
            exit_code, tile = self.machine.run_intcode()
            if exit_code:
                assert False
            self.tiles[(x, y)] = tile
            loop += 1
        score = self.tiles[(-1, 0)]
        del self.tiles[(-1, 0)]
        lx = min(self.tiles, key=lambda x: x[0])[0]
        ux = max(self.tiles, key=lambda x: x[0])[0]
        ly = min(self.tiles, key=lambda x: x[1])[1]
        uy = max(self.tiles, key=lambda x: x[1])[1]
        grid = [[self.tiles[(x, y)] for x in range(lx, ux+1)] for y in range(ly, uy + 1)]
        for i in range(len(grid)):
            row = []
            for element in grid[i]:
                if element == 4:
                    row.append('()')
                elif element == 3:
                    row.append('--')
                elif element == 2:
                    row.append('||')
                elif element == 1:
                    row.append('##')
                elif element == 0:
                    row.append('  ')
                else:
                    assert False
            grid[i] = ''.join(row)
        return score

    def move_towards_ball(self):
        for element in self.tiles:
            if self.tiles[element] == 4:
                ball = element[0]
            if self.tiles[element] == 3:
                paddle = element[0]
        if ball > paddle:
            return 1
        elif ball < paddle:
            return -1
        else:
            return 0


def play_game(data):
    game = Game(data)
    return game.play_game()


def main():
    year, day = 2019, 13
    data = get_data(year, day)
    print(start_game(data))
    print(play_game(data))


if __name__ == "__main__":
    main()
