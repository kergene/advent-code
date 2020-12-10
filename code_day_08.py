def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().replace('+','').splitlines()
    data = [instruction.split() for instruction in data]
    return data

def run_script(instructions):
    accumulator, row, seens = 0, 0, set()
    while row not in seens:
        seens.add(row)
        if instructions[row][0] == 'acc':
            accumulator += int(instructions[row][1])
            row += 1
        elif instructions[row][0] == 'jmp':
            row += int(instructions[row][1])
        elif instructions[row][0] == 'nop':
            row += 1
        else:
            raise ValueError()
    return accumulator

def test_fix(instructions):
    accumulator, row, seens = 0, 0, set()
    n = len(instructions)
    while row not in seens:
        if row == n:
            return accumulator
        seens.add(row)
        if instructions[row][0] == 'acc':
            accumulator += int(instructions[row][1])
            row += 1
        elif instructions[row][0] == 'jmp':
            row += int(instructions[row][1])
        elif instructions[row][0] == 'nop':
            row += 1
        else:
            raise Error()
    return 'Failed'

def de_corrupt(instructions):
    for row in range(len(instructions)):
        if instructions[row][0] == 'jmp':
            instructions[row][0] = 'nop'
            acc = test_fix(instructions)
            instructions[row][0] = 'jmp'
        elif instructions[row][0] == 'nop':
            instructions[row][0] = 'jmp'
            acc = test_fix(instructions)
            instructions[row][0] = 'nop'
        if acc != 'Failed':
            return acc

def main():
    day = 8
    instructions = get_data(day)
    print(run_script(instructions))
    print(de_corrupt(instructions))

if __name__ == "__main__":
    main()