from math import prod


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
            if line[2] in 'abcd':
                reg[line[2]] = reg[line[1]]
            i += 1
        elif line[0] == 'jnz':
            if reg[line[1]] != 0:
                i += reg[line[2]]
            else:
                i += 1
        elif line[0] == 'inc':
            reg[line[1]] += 1
            i += 1
        elif line[0] == 'dec':
            reg[line[1]] -= 1
            i += 1
        elif line[0] == 'tgl':
            tgl_idx = i + reg[line[1]]
            if 0 <= tgl_idx < len(data):
                tgl_line = data[tgl_idx]
                if len(tgl_line) == 2:
                    if tgl_line[0] == 'inc':
                        tgl_line[0] = 'dec'
                    else:
                        tgl_line[0] = 'inc'
                else:
                    if tgl_line[0] == 'jnz':
                        tgl_line[0] = 'cpy'
                    else:
                        tgl_line[0] = 'jnz'
            i += 1
        else:
            assert False
    return reg


def assembunny(data):
    data = [line.copy() for line in data]
    reg = Register({'a': 7, 'b': 0, 'c': 0, 'd': 0})
    reg = run_register(data, reg)
    return reg['a']


def assembunny_shortcut(data):
    # the input computes a!, and adds 75*85
    # this would take too long to compute on here
    reg = Register({'a': 12, 'b': 0, 'c': 0, 'd': 0})
    reg['a'] = prod(range(1, reg['a'] + 1)) + 75*85
    return reg['a']


def main():
    year, day = 2016, 23
    data = get_data(year, day)
    print(assembunny(data))
    print(assembunny_shortcut(data))


if __name__ == "__main__":
    main()
