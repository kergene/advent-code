from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(',')
    data = [int(datum) for datum in data]
    return data


class IntCode:
    def __init__(self, lines, droid=0):
        # the droid paramter is specific to this
        self.lines = lines.copy()
        self.index = 0
        self.relative_base = 0
        self.input = []
        self.input_index = 0
        self.droid = droid

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
                # these next two lines are specific to this
                if not self.input_index >= len(self.input):
                    self.droid.modify_location(self.input[self.input_index])
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


class RepairDroid:
    def __init__(self, data):
        self.machine = IntCode(data, self)
        self.grid = defaultdict(int)
        self.grid[(0 ,0)] = 'X'
        self.x = 0
        self.y = 0

    def run_droid(self, test_path):
        for step in test_path:
            exit_code, out = self.machine.run_intcode(step)
            if exit_code:
                assert False
            if out == 2:
                self.grid[(self.x, self.y)] = 'O'
            elif out == 1:
                if self.grid[(self.x, self.y)] == 'X':
                    continue
                self.grid[(self.x, self.y)] = '.'
            elif out == 0:
                self.grid[(self.x, self.y)] = '#'
        return self.grid[self.x, self.y]

    def modify_location(self, direction):
        if direction == 1:
            self.y += 1
        elif direction == 2:
            self.y -= 1
        elif direction == 3:
            self.x -= 1
        elif direction == 4:
            self.x += 1
        else:
            assert False


def find_o2(data):
    DIRECTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    start =  (0, 0)
    grid = defaultdict(int)
    routes = dict()
    routes[start] = (0, [])
    grid[start] = 'X'
    q = set()
    q.add(start)
    while q:
        x, y = choice = min(q, key=lambda pos: routes[pos][0])
        q.remove(choice)
        distance = routes[choice][0]
        path = routes[choice][1]
        for idx in range(len(DIRECTIONS)):
            dx, dy = DIRECTIONS[idx]
            pos = x + dx, y + dy
            if grid[pos] == 0: # i.e, if we haven't been here yet
                test_path = path + [idx + 1]
                droid = RepairDroid(data)
                grid[pos] = droid.run_droid(test_path)
                if grid[pos] == 'O':
                    return distance + 1
                elif grid[pos] == '.':
                    q.add(pos)
                    routes[pos] = (distance + 1, test_path)
    assert False


def fill_o2(data):
    DIRECTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    start =  (0, 0)
    grid = defaultdict(int)
    routes = dict()
    routes[start] = (0, [])
    grid[start] = 'X'
    q = set()
    q.add(start)
    while q:
        x, y = choice = min(q, key=lambda pos: routes[pos][0])
        q.remove(choice)
        distance = routes[choice][0]
        path = routes[choice][1]
        for idx in range(len(DIRECTIONS)):
            dx, dy = DIRECTIONS[idx]
            pos = x + dx, y + dy
            if grid[pos] == 0:
                # if we haven't seen the place before
                test_path = path + [idx + 1]
                droid = RepairDroid(data)
                grid[pos] = droid.run_droid(test_path)
                if grid[pos] == 'O' or grid[pos] == '.':
                    q.add(pos)
                    routes[pos] = (distance + 1, test_path)
    # flood fill grid with O2
    for pos, thing in grid.items():
        if thing == 'O':
            oxygen = pos
            break
    q = set()
    distances = dict()
    q.add(oxygen)
    distances[oxygen] = 0
    while q:
        x, y = choice = min(q, key=distances.get)
        q.remove(choice)
        distance = distances[choice]
        for dx, dy in DIRECTIONS:
            pos = x + dx, y + dy
            if grid[pos] == '.':
                grid[pos] = 'O'
                q.add(pos)
                distances[pos] = distance + 1
    return max(distances.values())


def main():
    year, day = 2019, 15
    data = get_data(year, day)
    print(find_o2(data))
    print(fill_o2(data))


if __name__ == "__main__":
    main()
