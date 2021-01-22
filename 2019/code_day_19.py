from collections import defaultdict
from itertools import product


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(',')
    data = [int(datum) for datum in data]
    return data


class IntCode:
    def __init__(self, lines):
        self.lines = lines.copy()
        self.index = 0
        self.relative_base = 0
        self.input = []
        self.input_index = 0

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


class TractorBeam:
    def __init__(self, data):
        self.machine = IntCode(data)
        self.view = []

    def test_droid(self, x, y):
        while True:
            exit_code, out = self.machine.run_intcode(x, y)
            if exit_code:
                return None
            else:
                return out


def test_cell(data, x, y):
    beam = TractorBeam(data)
    return beam.test_droid(x, y)


def detect_beam(data, x_lim, y_lim):
    # weird processing but allows for easy printing
    grid = [[0 for _ in range(x_lim)] for _ in range(y_lim)]
    for x, y in product(range(x_lim), range(y_lim)):
        grid[y][x] = '#' if test_cell(data, x, y) else '.'
    return sum(1 if char == '#' else 0 for row in grid for char in row)


def beam_count(data):
    return detect_beam(data, 50, 50)


def find_square(data, size):
    # note y = 4, x = 3 contains '#'
    x_min = 3
    x_max = 3
    y = 4
    while True:
        while True:
            if test_cell(data, x_min, y):
                break
            else:
                x_min += 1
        # x_min is first '#' in row y
        x_max = max(x_max, x_min + 100)
        while True:
            if test_cell(data, x_max, y):
                x_max += 1
            else:
                break
        # x_max - 1 is last '#' in row y (if >=100 in row)
        # so top left cell could be in x_min, ..., x_max - size + 1
        for x in range(x_min, x_max - size + 1):
            if test_cell(data, x, y + size - 1):
                return x * 10000 + y
        y += 1


def big_square(data):
    return find_square(data, 100)


def main():
    year, day = 2019, 19
    data = get_data(year, day)
    print(beam_count(data))
    print(big_square(data))


if __name__ == "__main__":
    main()
