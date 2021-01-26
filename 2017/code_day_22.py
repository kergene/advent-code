from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [list(datum) for datum in data]
    return data


def virus(data):
    grid = defaultdict(lambda: '.')
    n_rows = len(data)
    n_cols = len(data[0])
    sep_r = n_rows // 2
    sep_c = n_cols // 2
    for r in range(n_rows):
        for c in range(n_cols):
            grid[c - sep_c, r - sep_r] = data[r][c]
    x = y = 0
    DIRECTIONS = ((0, -1), (1, 0), (0, 1), (-1, 0))
    dir_idx = 0
    bursts = 0
    for _ in range(10 ** 4):
        if grid[x, y] == '#':
            dir_idx += 1
            grid[x, y] = '.'
        elif grid[x, y] == '.':
            bursts += 1
            dir_idx -= 1
            grid[x, y] = '#'
        dir_idx %= 4
        dx, dy = DIRECTIONS[dir_idx]
        x, y = x + dx, y + dy
    return bursts


def evolved(data):
    grid = defaultdict(lambda: '.')
    n_rows = len(data)
    n_cols = len(data[0])
    sep_r = n_rows // 2
    sep_c = n_cols // 2
    for r in range(n_rows):
        for c in range(n_cols):
            grid[c - sep_c, r - sep_r] = data[r][c]
    x = y = 0
    DIRECTIONS = ((0, -1), (1, 0), (0, 1), (-1, 0))
    dir_idx = 0
    bursts = 0
    for _ in range(10 ** 7):
        if grid[x, y] == 'W':
            bursts += 1
            grid[x, y] = '#'
        elif grid[x, y] == '#':
            dir_idx += 1
            grid[x, y] = 'F'
        elif grid[x, y] == 'F':
            dir_idx += 2
            grid[x, y] = '.'
        elif grid[x, y] == '.':
            dir_idx -= 1
            grid[x, y] = 'W'
        dir_idx %= 4
        dx, dy = DIRECTIONS[dir_idx]
        x, y = x + dx, y + dy
    return bursts


def main():
    year, day = 2017, 22
    data = get_data(year, day)
    print(virus(data))
    print(evolved(data))


if __name__ == "__main__":
    main()
