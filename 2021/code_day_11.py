def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return [int(val) for val in datum]


def take_step(data, nrows, ncols):
    DIRECTIONS = (
        (-1, -1), (-1,  0), (-1,  1),
        ( 0, -1), ( 0,  0), ( 0,  1),
        ( 1, -1), ( 1,  0), ( 1,  1)
    )
    nines = set()
    seen_nines = set()
    for r in range(nrows):
        for c in range(ncols):
            data[r, c] += 1
            if data[r, c] > 9:
                nines.add((r,c))
                seen_nines.add((r, c))
    while nines:
        r, c = nines.pop()
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (nr, nc) in data:
                if (nr, nc) not in seen_nines:
                    data[nr, nc] += 1
                    if data[nr, nc] > 9:
                        nines.add((nr,nc))
                        seen_nines.add((nr,nc))
    for pos in seen_nines:
        data[pos] = 0
    return data, len(seen_nines)


def flash_count(data):
    nrows = len(data)
    ncols = len(data[0])
    data_dict = {}
    for r in range(nrows):
        for c in range(ncols):
            data_dict[r, c] = data[r][c]
    flashes = 0
    for _ in range(100):
        data_dict, new_flashes = take_step(data_dict, nrows, ncols)
        flashes += new_flashes
    return flashes


def simultaneous_flash(data):
    nrows = len(data)
    ncols = len(data[0])
    data_dict = {}
    for r in range(nrows):
        for c in range(ncols):
            data_dict[r, c] = data[r][c]
    count = 0
    while True:
        count += 1
        data_dict, new_flashes = take_step(data_dict, nrows, ncols)
        if new_flashes == 100:
            break
    return count


def main():
    year, day = 2021, 11
    data = get_data(year, day)
    print(flash_count(data))
    print(simultaneous_flash(data))


if __name__ == "__main__":
    main()
