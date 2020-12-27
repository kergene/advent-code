def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().replace('+','').splitlines()
    data = [instruction.split() for instruction in data]
    return data


def run_script(instructions):
    accumulator, row, seens = 0, 0, {}
    while row not in seens:
        seens[row] = accumulator
        if instructions[row][0] == 'acc':
            accumulator += int(instructions[row][1])
            row += 1
        elif instructions[row][0] == 'jmp':
            row += int(instructions[row][1])
        elif instructions[row][0] == 'nop':
            row += 1
        else:
            raise ValueError()
    return accumulator, seens


def test_fix(instructions, row, accumulator, seens):
    seens.remove(row)
    n = len(instructions)
    while row not in seens:
        if row == n:
            return accumulator, seens
        seens.add(row)
        if instructions[row][0] == 'acc':
            accumulator += int(instructions[row][1])
            row += 1
        elif instructions[row][0] == 'jmp':
            row += int(instructions[row][1])
        elif instructions[row][0] == 'nop':
            row += 1
        else:
            raise ValueError
    else:
        return 'Failed', seens


def de_corrupt(instructions, seens):
    ever_seen = set(seens.keys())
    for row in seens:
        if instructions[row][0] == 'jmp':
            instructions[row][0] = 'nop'
            acc, ever_seen = test_fix(instructions, row, seens[row], ever_seen)
            instructions[row][0] = 'jmp'
        elif instructions[row][0] == 'nop':
            instructions[row][0] = 'jmp'
            acc, ever_seen = test_fix(instructions, row, seens[row], ever_seen)
            instructions[row][0] = 'nop'
        if acc != 'Failed':
            return acc


def main():
    year, day = 2020, 8
    instructions = get_data(year, day)
    accumulator, seens = run_script(instructions)
    print(accumulator)
    print(de_corrupt(instructions, seens))


if __name__ == "__main__":
    main()
