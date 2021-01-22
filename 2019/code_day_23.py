from collections import defaultdict
from itertools import product
from queue import SimpleQueue
from queue import Empty


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(',')
    data = [int(datum) for datum in data]
    return data


class IntCode:
    def __init__(self, network_address, lines):
        self.lines = lines.copy()
        self.index = 0
        self.relative_base = 0
        self.input = []
        self.input_index = 0
        # this is question-specifc
        self.network_address = network_address

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
        self.new_run = True
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
                # these next six lines are part of this game
                if self.input_index >= len(self.input):
                    self.input.append(self.network_address.get_input())
                if self.input[self.input_index] == -1:
                    if not self.new_run:
                        return 1, 0
                    self.new_run = False
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


class NetworkAddress:
    def __init__(self, network, data, address):
        self.input = SimpleQueue()
        if 0 <= address < 50:
            self.machine = IntCode(self, data)
            self.network = network
            self.input.put(address)

    def run_network(self):
        exit_code, address = self.machine.run_intcode()
        if exit_code:
            return -1
        exit_code, x = self.machine.run_intcode()
        if exit_code:
            assert False
        exit_code, y = self.machine.run_intcode()
        if exit_code:
            assert False
        if address not in self.network.components:
            self.network.components[address] = NetworkAddress(None, None, address)
        self.network.components[address].input.put(x)
        self.network.components[address].input.put(y)
        return address

    def get_input(self):
        try:
            value = self.input.get_nowait()
        except Empty:
            value = -1
        finally:
            return value


class Network:
    def __init__(self, data):
        self.components = dict()
        for idx in range(50):
            self.components[idx] = NetworkAddress(self, data, idx)

    def run(self, target):
        while True:
            for idx in range(50):
                self.components[idx].run_network()
                if target in self.components:
                    try:
                        self.components[target].input.get_nowait()
                        return self.components[target].input.get_nowait()
                    except Empty:
                        pass


def build_network(data):
    network = Network(data)
    return network.run(255)


class NATNetwork:
    def __init__(self, data):
        self.components = dict()
        self.last_x = -1
        self.last_y = -1
        for idx in range(50):
            self.components[idx] = NetworkAddress(self, data, idx)

    def run(self):
        nat_address = 255
        while True:
            sent = False
            for idx in range(50):
                address = self.components[idx].run_network()
                if address != -1:
                    sent = True
            if not sent:
                while True:
                    try:
                        x = self.components[nat_address].input.get_nowait()
                        y = self.components[nat_address].input.get_nowait()
                    except Empty:
                        break
                if self.last_x == x and self.last_y == y:
                    return y
                else:
                    self.last_x = x
                    self.last_y = y
                    self.components[0].input.put(x)
                    self.components[0].input.put(y)


def build_nat_network(data):
    network = NATNetwork(data)
    return network.run()


def main():
    year, day = 2019, 23
    data = get_data(year, day)
    print(build_network(data))
    print(build_nat_network(data))


if __name__ == "__main__":
    main()
