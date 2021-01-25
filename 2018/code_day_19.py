from sympy.ntheory import divisor_sigma


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [data[0]] + [preprocess(datum) for datum in data[1:]]
    return data


def preprocess(datum):
    datum = datum.split()
    eval_prefix = ''.join([datum[0], '(', ', '.join(datum[1:]), ', '])
    return eval_prefix


def addr(a, b, c, before):
    after = before.copy()
    after[c] = before[a] + before[b]
    return after


def addi(a, b, c, before):
    after = before.copy()
    after[c] = before[a] + b
    return after


def mulr(a, b, c, before):
    after = before.copy()
    after[c] = before[a] * before[b]
    return after


def muli(a, b, c, before):
    after = before.copy()
    after[c] = before[a] * b
    return after


def banr(a, b, c, before):
    after = before.copy()
    after[c] = before[a] & before[b]
    return after


def bani(a, b, c, before):
    after = before.copy()
    after[c] = before[a] & b
    return after


def borr(a, b, c, before):
    after = before.copy()
    after[c] = before[a] | before[b]
    return after


def bori(a, b, c, before):
    after = before.copy()
    after[c] = before[a] | b
    return after


def setr(a, b, c, before):
    after = before.copy()
    after[c] = before[a]
    return after


def seti(a, b, c, before):
    after = before.copy()
    after[c] = a
    return after


def gtir(a, b, c, before):
    after = before.copy()
    after[c] = int(a > before[b])
    return after


def gtri(a, b, c, before):
    after = before.copy()
    after[c] = int(before[a] > b)
    return after


def gtrr(a, b, c, before):
    after = before.copy()
    after[c] = int(before[a] > before[b])
    return after


def eqir(a, b, c, before):
    after = before.copy()
    after[c] = int(a == before[b])
    return after


def eqri(a, b, c, before):
    after = before.copy()
    after[c] = int(before[a] == b)
    return after


def eqrr(a, b, c, before):
    after = before.copy()
    after[c] = int(before[a] == before[b])
    return after


def base_program_shortcut(data, initial_0):
    # this gets the sum of divisors for some large number
    ip = int(data[0].split()[1])
    program = data[1:]
    register = [0] * 6
    register[0] = initial_0
    idx = 0
    while 0 <= register[ip] < len(program):
        idx += 1
        if register[5] == 3:
            break
        line = program[register[ip]]
        register = eval(line + 'register)')
        register[ip] += 1
    big_number = register[1]
    return divisor_sigma(big_number, 1)


def main():
    year, day = 2018, 19
    data = get_data(year, day)
    print(base_program_shortcut(data, 0))
    print(base_program_shortcut(data, 1))


if __name__ == "__main__":
    main()
