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


def shortest_program(data):
    # this program stops as soon as it hits the only row depending on 0
    ip = int(data[0].split()[1])
    program = data[1:]
    register = [0] * 6
    while 0 <= register[ip] < len(program):
        if register[ip] == 28:
            break
        line = program[register[ip]]
        register = eval(line + 'register)')
        register[ip] += 1
    return register[3]


def longest_program():
    # this uses values from the program directly
    set_val = 1397714
    mult = 65889
    reducer = 2 ** 24 - 1
    adder = 2 ** 16
    b = 0
    seens = set()
    while True:
        a = adder | b
        b = set_val
        while True:
            b += (a & 255)
            b &= reducer
            b *= mult
            b &= reducer
            if a < 256:
                break
            else:
                a //= 256
        if b not in seens:
            seens.add(b)
            last = b
        else:
            return last

def main():
    year, day = 2018, 21
    data = get_data(year, day)
    print(shortest_program(data))
    print(longest_program())


if __name__ == "__main__":
    main()
