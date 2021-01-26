from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum.split()


class RegisterMachine:
    def __init__(self, data):
        self.lines = data
        self.line_idx = 0
        self.registers = defaultdict(int)
        self.NUMERIC = '-0123456789'
    
    def run_program(self):
        self.running = True
        while self.running:
            self.run_line()
        return self.last_played

    def run_line(self):
        self.current_line = self.lines[self.line_idx]
        if self.current_line[0] == 'snd':
            self.snd()
        elif self.current_line[0] == 'set':
            self.val()
        elif self.current_line[0] == 'add':
            self.add()
        elif self.current_line[0] == 'mul':
            self.mul()
        elif self.current_line[0] == 'mod':
            self.mod()
        elif self.current_line[0] == 'rcv':
            self.rcv()
        elif self.current_line[0] == 'jgz':
            self.jgz()
        else:
            assert False, self.current_line[0]
    
    def snd(self):
        val = self.current_line[1]
        if val[0] in self.NUMERIC:
            self.last_played = int(val)
        else:
            self.last_played = self.registers[val]
        self.line_idx += 1

    def val(self):
        val = self.current_line[2]
        if val[0] in self.NUMERIC:
            self.registers[self.current_line[1]] = int(val)
        else:
            self.registers[self.current_line[1]] = self.registers[val]
        self.line_idx += 1

    def add(self):
        val = self.current_line[2]
        if val[0] in self.NUMERIC:
            self.registers[self.current_line[1]] += int(val)
        else:
            self.registers[self.current_line[1]] += self.registers[val]
        self.line_idx += 1

    def mul(self):
        val = self.current_line[2]
        if val[0] in self.NUMERIC:
            self.registers[self.current_line[1]] *= int(val)
        else:
            self.registers[self.current_line[1]] *= self.registers[val]
        self.line_idx += 1

    def mod(self):
        val = self.current_line[2]
        if val[0] in self.NUMERIC:
            self.registers[self.current_line[1]] %= int(val)
        else:
            self.registers[self.current_line[1]] %= self.registers[val]
        self.line_idx += 1

    def rcv(self):
        val = self.current_line[1]
        if val[0] in self.NUMERIC:
            test_val = int(val)
        else:
            test_val = self.registers[val]
        if test_val != 0:
            self.running = False
        else:
            self.line_idx += 1

    def jgz(self):
        val = self.current_line[1]
        if val[0] in self.NUMERIC:
            test_val = int(val)
        else:
            test_val = self.registers[val]
        if test_val > 0:
            jump_val = self.current_line[2]
            if jump_val[0] in self.NUMERIC:
                self.line_idx += int(jump_val)
            else:
                self.line_idx += self.registers[jump_val]
        else:    
            self.line_idx += 1


def single_machine(data):
    reg = RegisterMachine(data)
    return reg.run_program()


class DuetMachine:
    def __init__(self, data, pid):
        # first line not needed
        self.pid = pid
        self.lines = data
        self.line_idx = 0
        self.registers = defaultdict(int)
        self.registers['p'] = pid
        self.received = []
        self.NUMERIC = '-0123456789'
        self.sent_values = 0
    
    def __repr__(self):
        return 'DuetMachine ' + str(self.pid)

    def set_other(self, other):
        self.other = other
    
    def run_program(self):
        self.running = True
        while self.running:
            self.run_line()

    def run_line(self):
        self.current_line = self.lines[self.line_idx]
        if self.current_line[0] == 'snd':
            self.snd()
        elif self.current_line[0] == 'set':
            self.val()
        elif self.current_line[0] == 'add':
            self.add()
        elif self.current_line[0] == 'mul':
            self.mul()
        elif self.current_line[0] == 'mod':
            self.mod()
        elif self.current_line[0] == 'rcv':
            self.rcv()
        elif self.current_line[0] == 'jgz':
            self.jgz()
        else:
            assert False, self.current_line[0]
    
    def snd(self):
        val = self.current_line[1]
        if val[0] in self.NUMERIC:
            self.other.received.append(int(val))
        else:
            self.other.received.append(self.registers[val])
        self.line_idx += 1
        self.sent_values += 1

    def val(self):
        val = self.current_line[2]
        if val[0] in self.NUMERIC:
            self.registers[self.current_line[1]] = int(val)
        else:
            self.registers[self.current_line[1]] = self.registers[val]
        self.line_idx += 1

    def add(self):
        val = self.current_line[2]
        if val[0] in self.NUMERIC:
            self.registers[self.current_line[1]] += int(val)
        else:
            self.registers[self.current_line[1]] += self.registers[val]
        self.line_idx += 1

    def mul(self):
        val = self.current_line[2]
        if val[0] in self.NUMERIC:
            self.registers[self.current_line[1]] *= int(val)
        else:
            self.registers[self.current_line[1]] *= self.registers[val]
        self.line_idx += 1

    def mod(self):
        val = self.current_line[2]
        if val[0] in self.NUMERIC:
            self.registers[self.current_line[1]] %= int(val)
        else:
            self.registers[self.current_line[1]] %= self.registers[val]
        self.line_idx += 1

    def rcv(self):
        val = self.current_line[1]
        if self.received:
            self.registers[val] = self.received.pop(0)
            self.line_idx += 1
        else:
            self.running = False

    def jgz(self):
        val = self.current_line[1]
        if val[0] in self.NUMERIC:
            test_val = int(val)
        else:
            test_val = self.registers[val]
        if test_val > 0:
            jump_val = self.current_line[2]
            if jump_val[0] in self.NUMERIC:
                self.line_idx += int(jump_val)
            else:
                self.line_idx += self.registers[jump_val]
        else:    
            self.line_idx += 1


class Duet:
    def __init__(self, data):
        self.machines = []
        for pid in range(2):
            self.machines.append(DuetMachine(data, pid))
        for pid in range(2):
            self.machines[pid].set_other(self.machines[1 - pid])

    def run_duet(self):
        check = (
            bool(self.machines[0].received) or
            self.machines[1].received or
            not self.machines[0].sent_values or
            not self.machines[1].sent_values
        )
        while check:
            for pid in range(2):
                if self.machines[pid].received or not self.machines[pid].sent_values:
                    self.machines[pid].run_program()
            check = (
                bool(self.machines[0].received) or
                self.machines[1].received or
                not self.machines[0].sent_values or
                not self.machines[1].sent_values
            )
        return self.machines[1].sent_values


def double_machine(data):
    duet = Duet(data)
    return duet.run_duet()


def main():
    year, day = 2017, 18
    data = get_data(year, day)
    print(single_machine(data))
    print(double_machine(data))


if __name__ == "__main__":
    main()
