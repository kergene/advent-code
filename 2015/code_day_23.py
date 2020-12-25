def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum.replace('a', '0').replace('b', '1')


def run(data, init_a, init_b):
    reg = [init_a, init_b]
    line_number = 0
    n = len(data)
    while line_number < n:
        line = data[line_number].split()
        if line[0] == 'hlf':
            reg[int(line[1])] //= 2
            line_number += 1
        elif line[0] == 'tpl':
            reg[int(line[1])] *= 3
            line_number += 1
        elif line[0] == 'inc':
            reg[int(line[1])] += 1
            line_number += 1
        elif line[0] == 'jmp':
            line_number += int(line[1])
        elif line[0] == 'jie':
            if reg[int(line[1][:-1])] % 2 == 0:
                line_number += int(line[2])
            else:
                line_number += 1
        elif line[0] == 'jio':
            if reg[int(line[1][:-1])] == 1:
                line_number += int(line[2])
            else:
                line_number += 1
        else:
            assert False
    return reg[1]


def main():
    year, day = 2015, 23
    data = get_data(year, day)
    print(run(data, 0, 0))
    print(run(data, 1, 0))


if __name__ == "__main__":
    main()
