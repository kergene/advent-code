import numpy as np


# part 2 takes a couple of mins
def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return int(datum)


def get_pattern(idx):
    BASE = [0, 1, 0, -1]
    pattern = [value for value in BASE for _ in range(idx + 1)]
    return pattern


def flawed_frequency_transmission(data):
    new_data = []
    for idx in range(len(data)):
        pattern = get_pattern(idx)
        n = len(pattern)
        tot = 0
        for sum_idx in range(len(data)):
            tot += data[sum_idx] * pattern[(sum_idx + 1) % n]
        value = int(str(tot)[-1])
        new_data.append(value)
    return new_data


def message_start(data):
    for _ in range(100):
        data = flawed_frequency_transmission(data)
    return ''.join(str(val) for val in data[:8])


def embedded_message(data):
    offset = int(''.join(str(val) for val in data[:7]))
    data = [val for _ in range(10000) for val in data]
    n = len(data) // 2
    data = data[n:]
    offset -= n
    for _ in range(100):
        data = flawed_frequency_transmission_offset(data, n)
    return ''.join(str(val) for val in data[offset:offset + 8])


def flawed_frequency_transmission_offset(data, n):
    new_data = [0] * n
    new_data[-1] = data[-1]
    for idx in range(1, n):
        new_data[-idx - 1] = int(str(new_data[-idx] + data[-idx - 1])[-1])
    return new_data


def main():
    year, day = 2019, 16
    data = get_data(year, day)
    print(message_start(data))
    print(embedded_message(data))


if __name__ == "__main__":
    main()
