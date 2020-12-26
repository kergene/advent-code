def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return [int(i) for i in data]


def generate_checksum(a, length):
    while len(a) < length:
        a += [0] + [1 - a[-i-1] for i in range(len(a))]
    a = a[:length]
    while len(a) % 2 == 0:
        a = [int(a[i] == a[i+1]) for i in range(0, len(a), 2)]
    return ''.join(str(i) for i in a)


def find_small_checksum(data):
    length = 272
    return generate_checksum(data, length)


def find_large_checksum(data):
    length = 35651584
    return generate_checksum(data, length)


def main():
    year, day = 2016, 16
    data = get_data(year, day)
    print(find_small_checksum(data))
    print(find_large_checksum(data))


if __name__ == "__main__":
    main()
