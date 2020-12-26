from numpy import base_repr


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return int(data)


def preprocess(datum):
    return datum


def steal_left(data):
    return int(bin(data)[3:] + '1', 2)


def steal_across(data):
    base_3 = base_repr(data, 3)
    rest = base_3[1:]
    if base_3[0] == '1':
        return int(rest, 3)
    else:
        return int(rest, 3) + int('1' + rest, 3)


def main():
    year, day = 2016, 19
    data = get_data(year, day)
    print(steal_left(data))
    print(steal_across(data))


if __name__ == "__main__":
    main()
