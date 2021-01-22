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
        in_idx = 0
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
                self.set_val(self.index + 1, params[-1], p_in[in_idx])
                in_idx += 1
                self.index += param_length + 1
            elif instruction == 4:
                param_length = 1
                params = params.zfill(param_length)
                output = self.get_val(self.index + 1, params[-1])
                self.index += param_length + 1
                return output, 0
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
        return p_in, 1


def get_boost(data):
    boost = IntCode(data)
    output = []
    while True:
        out, exit_code = boost.run_intcode(1)
        if exit_code:
            break
        else:
            output.append(out)
    assert len(output) == 1, 'Too many outputs'
    return output[0]


def distress_coords(data):
    boost = IntCode(data)
    output = []
    while True:
        out, exit_code = boost.run_intcode(2)
        if exit_code:
            break
        else:
            output.append(out)
    assert len(output) == 1, 'Too many outputs'
    return output[0]


def main():
    year, day = 2019, 9
    data = get_data(year, day)
    print(get_boost(data))
    print(distress_coords(data))


if __name__ == "__main__":
    main()
