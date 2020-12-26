from sympy.ntheory.modular import crt


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = datum.split()
    return [int(datum[3]), int(datum[-1][:-1])]


def win_capsule(data):
    data = [item.copy() for item in data]
    for i in range(len(data)):
        data[i][1] = data[i][0] - data[i][1] - i - 1
    data = list(zip(*data))
    return crt(data[0], data[1])[0]


def win_extra_capsule(data):
    data.append([11,0])
    return win_capsule(data)


def main():
    year, day = 2016, 15
    data = get_data(year, day)
    print(win_capsule(data))
    print(win_extra_capsule(data))


if __name__ == "__main__":
    main()
