def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return data


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


def ones_count(data):
    data += '-'
    tot = 0
    for idx in range(128):
        tot += sum(int(val) for val in format(int(knot_hash(data + str(idx)), 16), 'b'))
    return tot


def component_count(data):
    data += '-'
    grid = []
    for idx in range(128):
        to_hash = data + str(idx)
        hashed = knot_hash(to_hash)
        grid.append(format(int(hashed, 16), 'b').zfill(128))
    # convert to set of values with a 1
    ones = set((x,y) for x in range(128) for y in range(128) if int(grid[y][x]))
    DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    group_count = 0
    while ones:
        group_count += 1
        group_choice = ones.pop()
        q = set()
        q.add(group_choice)
        while q:
            x, y = q.pop()
            for dx, dy in DIRECTIONS:
                pos = x + dx, y + dy
                if pos in ones:
                    q.add(pos)
                    ones.remove(pos)
    return group_count


def main():
    year, day = 2017, 14
    data = get_data(year, day)
    print(ones_count(data))
    print(component_count(data))


if __name__ == "__main__":
    main()
