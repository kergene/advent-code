def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum.split()


class Register(dict):
    def __missing__(self, value):
        return int(value)


def run_register(data, reg):
    i = 0
    while i < len(data):
        line = data[i]
        if line[0] == 'cpy':
            reg[line[2]] = reg[line[1]]
            i += 1
        elif line[0] == 'jnz':
            if reg[line[1]] != 0:
                i += int(line[2])
            else:
                i += 1
        elif line[0] == 'inc':
            reg[line[1]] += 1
            i += 1
        elif line[0] == 'dec':
            reg[line[1]] -= 1
            i += 1
        else:
            assert False
    return reg


def assembunny(data):
    reg = Register({'a': 0, 'b': 0, 'c': 0, 'd': 0})
    reg = run_register(data, reg)
    return reg['a']


def set_ignition(data):
    reg = Register({'a': 0, 'b': 0, 'c': 1, 'd': 0})
    reg = run_register(data, reg)
    return reg['a']


def main():
    year, day = 2016, 12
    data = get_data(year, day)
    print(assembunny(data))
    print(set_ignition(data))


if __name__ == "__main__":
    main()
