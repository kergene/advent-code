from sympy import isprime


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum.split()


def run(data):
    REG_KEYS = 'abcdefgh'
    registers = dict((register, 0) for register in REG_KEYS)
    n = len(data)
    mul_count = 0
    line_idx = 0
    while 0 <= line_idx < n:
        instruction, target, val = data[line_idx]
        if val in REG_KEYS:
            val = registers[val]
        else:
            val = int(val)
        if instruction == 'set':
            registers[target] = val
            line_idx += 1
        elif instruction == 'sub':
            registers[target] -= val
            line_idx += 1
        elif instruction == 'mul':
            registers[target] *= val
            mul_count += 1
            line_idx += 1
        elif instruction == 'jnz':
            if target in REG_KEYS:
                target = registers[target]
            else:
                target = int(target)
            if target != 0:
                line_idx += val
            else:
                line_idx += 1
        else:
            assert False, instruction
    return mul_count


def composite_count(data):
    # this gets number of composite numbers in
    # (107900, 107917, 107934, 107951, ..., 124900)
    composites = 0
    for idx in range(107900, 124901, 17):
        if not isprime(idx):
            composites += 1
    return composites


def main():
    year, day = 2017, 23
    data = get_data(year, day)
    print(run(data))
    print(composite_count(data))


if __name__ == "__main__":
    main()
