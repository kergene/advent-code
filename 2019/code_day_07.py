from itertools import permutations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(',')
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return int(datum)

class IntCode:
    def __init__(self, lines):
        self.lines = lines.copy()
        self.index = 0

    def get_val(self, index, parameter):
        if parameter == '1':
            return self.lines[index]
        else:
            return self.lines[self.lines[index]]

    def set_val(self, index, parameter, value):
        if parameter == '1':
            self.lines[index] = value
        else:
            self.lines[self.lines[index]] = value

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
            else:
                assert False, instruction
        return p_in, 1


def amplify_thrust(data):
    max_thrust = 0
    for phase in permutations(range(5)):
        amplifiers = [IntCode(data) for i in range(5)]
        p_in = 0
        for i in range(5):
            p_in, _ = amplifiers[i].run_intcode(phase[i], p_in)
        if p_in > max_thrust:
            max_thrust = p_in
    return max_thrust


def re_amplify_thrust(data):
    max_thrust = -1
    for phase in permutations(range(5, 10)):
        amplifiers = [IntCode(data) for i in range(5)]
        p_in = 0
        loop = 0
        while True:
            for i in range(5):
                if loop:
                    p_in, exit_code = amplifiers[i].run_intcode(p_in)
                else:
                    p_in, exit_code = amplifiers[i].run_intcode(phase[i], p_in)
                if exit_code:
                    break
            if exit_code:
                if p_in[0] > max_thrust:
                    max_thrust = p_in[0]
                break
            loop += 1
    return max_thrust


def main():
    year, day = 2019, 7
    data = get_data(year, day)
    print(amplify_thrust(data))
    print(re_amplify_thrust(data))


if __name__ == "__main__":
    main()
