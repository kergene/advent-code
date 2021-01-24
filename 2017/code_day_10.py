def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return data


def knot_round(data):
    n = 256
    data = [int(datum) for datum in data.split(',')]
    contents = list(range(n))
    position = 0
    skip_size = 0
    for length in data:
        for i in range(length // 2):
            contents[(position + i) % n], contents[(position + length - i - 1) % n] = contents[(position + length - i - 1) % n], contents[(position + i) % n]
        position += length + skip_size
        skip_size += 1
    return contents[0] * contents[1]


def knot_hash(data):
    extra_lengths = [17, 31, 73, 47, 23]
    n = 256
    data = [ord(datum) for datum in data]
    data += extra_lengths
    contents = list(range(n))
    position = 0
    skip_size = 0
    for _ in range(64):
        for length in data:
            for i in range(length // 2):
                contents[(position + i) % n], contents[(position + length - i - 1) % n] = contents[(position + length - i - 1) % n], contents[(position + i) % n]
            position += length + skip_size
            skip_size += 1
    dense = []
    for idx in range(16):
        xor = contents[idx * 16]
        for val in contents[idx * 16 + 1:idx * 16 + 16]:
            xor ^= val
        dense.append(xor)
    return ''.join([format(val, 'x').zfill(2) for val in dense])


def main():
    year, day = 2017, 10
    data = get_data(year, day)
    print(knot_round(data))
    print(knot_hash(data))


if __name__ == "__main__":
    main()
