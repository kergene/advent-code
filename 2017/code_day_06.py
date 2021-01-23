def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split()
    data = [int(datum) for datum in data]
    return data


def debug(data):
    # deliberatly mutating data
    seens = set()
    n = len(data)
    while True:
        hashable = tuple(data)
        if hashable in seens:
            break
        else:
            seens.add(hashable)
        redist_idx = max(range(n), key=lambda i: (data[i], n - i))
        redist_count = data[redist_idx]
        data[redist_idx] = 0
        for _ in range(redist_count):
            redist_idx += 1
            redist_idx %= n
            data[redist_idx] += 1
    return len(seens)


def main():
    year, day = 2017, 6
    data = get_data(year, day)
    print(debug(data))
    print(debug(data))


if __name__ == "__main__":
    main()
