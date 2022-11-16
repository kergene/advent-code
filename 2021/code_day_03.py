def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return [int(i) for i in datum]


def power_consumption(data):
    data = zip(*data)
    bits = []
    for row in data:
        if 2 * sum(row) > len(row):
            bits.append('1')
        else:
            bits.append('0')
    twos = len(bits)
    binary = int(''.join(bits), 2)
    return (2 ** twos - binary - 1) * binary


def life_support_rating(data):
    index = 0
    new_data = data
    while len(new_data) > 1:
        count = sum(row[index] for row in new_data)
        if 2 * count < len(new_data):
            next_data = []
            for row in new_data:
                if row[index] == 0:
                    next_data.append(row)
            new_data = next_data
        else:
            next_data = []
            for row in new_data:
                if row[index] == 1:
                    next_data.append(row)
            new_data = next_data
        index += 1
    o2 = int(''.join(str(element) for element in new_data[0]), 2)
    index = 0
    new_data = data
    while len(new_data) > 1:
        count = sum(row[index] for row in new_data)
        if 2 * count < len(new_data):
            next_data = []
            for row in new_data:
                if row[index] == 1:
                    next_data.append(row)
            new_data = next_data
        else:
            next_data = []
            for row in new_data:
                if row[index] == 0:
                    next_data.append(row)
            new_data = next_data
        index += 1
    co2 = int(''.join(str(element) for element in new_data[0]), 2)
    return o2 * co2


def main():
    year, day = 2021, 3
    data = get_data(year, day)
    print(power_consumption(data))
    print(life_support_rating(data))


if __name__ == "__main__":
    main()
