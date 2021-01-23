import numpy as np
from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return int(data)


def spiral_dist(data):
    n = int(np.sqrt(data))
    x_displacement = (n - 1) // 2
    y_displacement = (n - 1) - x_displacement
    remaining = data - n ** 2
    if remaining > 0:
        x_displacement += 1
        if remaining > n + 1:
            remaining = remaining - n - 1
            x_displacement -= remaining
        else:
            y_displacement -= remaining - 1
    return abs(x_displacement) + abs(y_displacement)


def adjacent_sums(data):
    NEIGHBOURS = (
        (-1, -1), (-1,  0), (-1, 1),
        ( 0, -1),           ( 0, 1),
        ( 1, -1), ( 1,  0), ( 1, 1)
    )
    DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
    grid = defaultdict(int)
    grid[0, 0] = 1
    x = y = 0
    dir_idx = 0
    length = 1
    remaining = length
    while True:
        if grid[x, y] > data:
            return grid[x, y]
        else:
            # add next element
            dx, dy = DIRECTIONS[dir_idx]
            x += dx
            y += dy
            grid[x, y] = sum(grid[x + dx, y + dy] for dx, dy in NEIGHBOURS)
            remaining -= 1
            if remaining == 0:
                # start next line
                # reset direction
                dir_idx += 1
                dir_idx %= 4
                # reset counter
                if dir_idx % 2:
                    remaining = length
                else:
                    length += 1
                    remaining = length


def main():
    year, day = 2017, 3
    data = get_data(year, day)
    print(spiral_dist(data))
    print(adjacent_sums(data))


if __name__ == "__main__":
    main()
