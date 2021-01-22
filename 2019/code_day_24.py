from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return [int(element == '#') for element in datum]


def get_biodiversity(grid):
    grid = [str(element) for row in grid.copy() for element in row][::-1]
    return int(''.join(grid), 2)


def update_from_neighbours(r, c, grid, n_rows, n_cols):
    DIRECTIONS = ((1,0), (-1,0), (0,1), (0,-1))
    counter = 0
    for dr, dc in DIRECTIONS:
        a, b = r + dr, c + dc
        if 0 <= a < n_rows and 0 <= b < n_cols:
            counter += grid[a][b]
    if counter == 1:
        return 1
    elif counter == 2 and grid[r][c] == 0:
        return 1
    else:
        return 0


def take_step(grid, n_rows, n_cols):
    new_grid = [[update_from_neighbours(r, c, grid, n_rows, n_cols) for c in range(n_cols)] for r in range(n_rows)]
    return new_grid


def bug_tracking(grid):
    n_rows = len(grid)
    n_cols = len(grid[0])
    seen_bios = set()
    while True:
        bio = get_biodiversity(grid)
        if bio in seen_bios:
            return bio
        else:
            seen_bios.add(bio)
            grid = take_step(grid, n_rows, n_cols)


def take_layered_step(active):
    DIRECTIONS = ((1,0), (-1,0), (0,1), (0,-1))
    new_active = set()
    neighbours = defaultdict(int)
    for cell in active:
        layer, r, c = cell
        for dr, dc in DIRECTIONS:
            a, b = r + dr, c + dc
            if 0 <= a < 5 and 0 <= b < 5:
                if (a, b) != (2,2):
                    neighbours[(layer, a, b)] += 1
        if r == 0:
            neighbours[(layer - 1, 1, 2)] += 1
        if r == 4:
            neighbours[(layer - 1, 3, 2)] += 1
        if c == 0:
            neighbours[(layer - 1, 2, 1)] += 1
        if c == 4:
            neighbours[(layer - 1, 2, 3)] += 1
        if (r,c) == (1,2):
            for b in range(5):
                neighbours[(layer + 1, 0, b)] += 1
        if (r,c) == (2,1):
            for a in range(5):
                neighbours[(layer + 1, a, 0)] += 1
        if (r,c) == (3,2):
            for b in range(5):
                neighbours[(layer + 1, 4, b)] += 1
        if (r,c) == (2,3):
            for a in range(5):
                neighbours[(layer + 1, a, 4)] += 1
    for cell, value in neighbours.items():
        if value == 1:
            new_active.add(cell)
        elif value == 2 and cell not in active:
            new_active.add(cell)
    return new_active


def recursive_bug_tracking(grid):
    loops = 200
    n_rows = len(grid)
    n_cols = len(grid[0])
    active = set()
    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c]:
                active.add((0, r, c))
    for _ in range(loops):
        active = take_layered_step(active)
    return len(active)


def main():
    year, day = 2019, 24
    data = get_data(year, day)
    print(bug_tracking(data))
    print(recursive_bug_tracking(data))


if __name__ == "__main__":
    main()
