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


def run_register(data, reg, terminate=0):
    i = 0
    j = 0
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
        elif line[0] == 'out':
            print(reg['b'])
            i += 1
            j += 1
            if 0 < terminate <= j:
                return True
            if reg['b'] not in (0, 1):
                return False
        else:
            assert False


def assembunny(data, n, terminate=0):
    # kept in for reference
    # using n = 175 can see output as desired
    # terminates after term outputs if non-zero
    reg = Register({'a': n, 'b': 0, 'c': 0, 'd': 0})
    reg = run_register(data, reg, terminate)
    return reg


def find_clock(data):
    # this actually just finds the first
    # binary number of the form:
    # 1010..10 greater than 365*7
    i = 0
    while True:
        n = i + 7*365
        while n > 0:
            if n % 2 == 0:
                n //= 2
                if n % 2 == 1:
                    n //=2
                else:
                    break
            else:
                break
        if n == 0:
            break
        i += 1
    return i


def main():
    year, day = 2016, 25
    data = get_data(year, day)
    print(find_clock(data))
#    assembunny(data, 99)


if __name__ == "__main__":
    main()
