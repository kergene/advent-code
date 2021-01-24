from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = datum.split()
    return datum


def max_reg_final(data):
    registers = defaultdict(int)
    for line in data:
        condition = 'registers["' + line[-3] + '"]' + line[-2] + line[-1]
        if eval(condition):
            if line[1] == 'inc':
                registers[line[0]] += int(line[2])
            else:
                registers[line[0]] -= int(line[2])
    return max(registers.values())


def max_reg_ever(data):
    registers = defaultdict(int)
    max_reg = -float('inf')
    for line in data:
        condition = 'registers["' + line[-3] + '"]' + line[-2] + line[-1]
        if eval(condition):
            if line[1] == 'inc':
                registers[line[0]] += int(line[2])
            else:
                registers[line[0]] -= int(line[2])
            if registers[line[0]] > max_reg:
                max_reg = registers[line[0]]
    return max_reg


def main():
    year, day = 2017, 8
    data = get_data(year, day)
    print(max_reg_final(data))
    print(max_reg_ever(data))


if __name__ == "__main__":
    main()
