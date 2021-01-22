from itertools import product


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(',')
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return int(datum)


def run_intcode(lines):
    i = 0
    while True:
        if lines[i] == 99:
            break
        elif lines[i] == 1:
            lines[lines[i+3]] = lines[lines[i + 1]] + lines[lines[i + 2]]
            i += 4
        elif lines[i] == 2:
            lines[lines[i+3]] = lines[lines[i + 1]] * lines[lines[i + 2]]
            i += 4
        else:
            assert False


def run_1202(data):
    lines = data.copy()
    lines[1] = 12
    lines[2] = 2
    run_intcode(lines)
    return lines[0]


def find_memory_state(data):
    TARGET = 19690720
    for i in product(range(100), repeat=2):
        a = i[0]
        b = i[1]
        lines = data.copy()
        lines[1] = a
        lines[2] = b
        run_intcode(lines)
        if lines[0] == TARGET:
            return 100*a + b


def main():
    year, day = 2019, 2
    data = get_data(year, day)
    print(run_1202(data))
    print(find_memory_state(data))


if __name__ == "__main__":
    main()
