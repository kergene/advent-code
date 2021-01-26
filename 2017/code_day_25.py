from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    initial_state, checksum_time = preprocess_start(data[0])
    instructions = dict(preprocess(datum) for datum in data[1:])
    return initial_state, checksum_time, instructions


def preprocess_start(datum):
    datum = datum.splitlines()
    initial_state = datum[0][-2]
    checksum_time = int(datum[1].split()[-2])
    return initial_state, checksum_time


def preprocess(datum):
    datum = datum.splitlines()
    state = datum[0][-2]
    datum = datum[1:]
    d = dict()
    for idx in range(2):
        current = int(datum[4*idx][-2])
        write = int(datum[4*idx + 1][-2])
        direction = datum[4*idx + 2].split()[-1][:-1]
        next_state = datum[4*idx + 3][-2]
        d[current] = {'val': write, 'step': direction, 'next': next_state}
    return state, d


def turing_machine(initial_state, checksum_time, instructions):
    tape = defaultdict(int)
    state = initial_state
    cursor = 0
    t = 0
    while t < checksum_time:
        t += 1
        rule = instructions[state][tape[cursor]]
        tape[cursor] = rule['val']
        cursor += 1 if rule['step'] == 'right' else -1
        state = rule['next']
    return sum(tape.values())


def main():
    year, day = 2017, 25
    initial_state, checksum_time, instructions = get_data(year, day)
    print(turing_machine(initial_state, checksum_time, instructions))


if __name__ == "__main__":
    main()
