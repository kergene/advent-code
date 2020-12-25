from itertools import product


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [list(datum) for datum in data]
    return data


def conway_3d(data):
    iters = 6
    n = len(data)
    zeros = [['.' for i in range(n + iters*2)] for j in range(n + iters*2)]
    TRIPLET = (-1,0,1)
    DIRECTIONS = []
    for i in product(TRIPLET, repeat=3):
        if i != (0,0,0):
            DIRECTIONS += [i]
    grid = copy_2d(zeros)
    for i in range(n):
        for j in range(n):
            grid[i + iters][j + iters] = data[i][j]
    # create 3d grid
    grid = [grid]
    for cycle in range(iters):
        grid = [zeros] + grid + [zeros]
    for cycle in range(iters):
        tot = 0
        new_grid = copy_3d(grid)
        for x in range(iters - cycle - 1, iters + n + cycle + 1):
            for y in range(iters - cycle - 1, iters + n + cycle + 1):
                for z in range(iters - cycle - 1, iters + cycle + 2):
                    count = 0
                    for dx, dy, dz in DIRECTIONS:
                        a,b,c = x+dx, y+dy, z+dz
                        if 0 <= a < n + iters*2 and 0 <= b < n + iters*2 and 0 <= c < 1 + iters*2:
                            if grid[c][b][a] == '#':
                                count += 1
                                if count > 3:
                                    break
                    if grid[z][y][x] == '#' and count in (2,3):
                        new_grid[z][y][x] = '#'
                        tot += 1
                    elif grid[z][y][x] == '.' and count == 3:
                        new_grid[z][y][x] = '#'
                        tot += 1
                    else:
                        new_grid[z][y][x] = '.'
        grid = new_grid
    return tot


def conway_4d(data):
    iters = 6
    n = len(data)
    zeros_2d = [['.' for i in range(n + iters*2)] for j in range(n + iters*2)]
    zeros_3d = [[['.' for i in range(n + iters*2)] for j in range(n + iters*2)] for k in range(13)]
    TRIPLET = (-1,0,1)
    DIRECTIONS = []
    for i in product(TRIPLET, repeat=4):
        if i != (0,0,0,0):
            DIRECTIONS += [i]
    grid = copy_2d(zeros_2d)
    for i in range(n):
        for j in range(n):
            grid[i + iters][j + iters] = data[i][j]
    # create 3d grid
    grid = [grid]
    for cycle in range(iters):
        grid = [zeros_2d] + grid + [zeros_2d]
    # create 4d grid
    grid = [grid]
    for cycle in range(iters):
        grid = [(zeros_3d)] + grid + [(zeros_3d)]
    for cycle in range(iters):
        tot = 0
        new_grid = copy_4d(grid)
        for x in range(iters - cycle - 1, iters + n + cycle + 1):
            for y in range(iters - cycle - 1, iters + n + cycle + 1):
                for z in range(iters - cycle - 1, iters + cycle + 2):
                    for w in range(iters - cycle - 1, iters + cycle + 2):
                        count = 0
                        for dx, dy, dz, dw in DIRECTIONS:
                            a,b,c,d = x+dx, y+dy, z+dz, w+dw
                            if 0 <= a < n + iters*2 and 0 <= b < n + iters*2 and 0 <= c < 1 + iters*2 and 0 <= d < 1 + iters*2:
                                if grid[d][c][b][a] == '#':
                                    count += 1
                                    if count > 3:
                                        break
                        if grid[w][z][y][x] == '#' and count in (2,3):
                            new_grid[w][z][y][x] = '#'
                            tot += 1
                        elif grid[w][z][y][x] == '.' and count == 3:
                            new_grid[w][z][y][x] = '#'
                            tot += 1
                        else:
                            new_grid[w][z][y][x] = '.'
        grid = new_grid
    return tot


def copy_2d(grid):
    return [row.copy() for row in grid]


def copy_3d(grid):
    return [[row.copy() for row in layer] for layer in grid]


def copy_4d(grid):
    return [[[row.copy() for row in layer] for layer in multilayer] for multilayer in grid]


def main():
    year, day = 2020, 17
    data = get_data(year, day)
    print(conway_3d(data))
    print(conway_4d(data))


if __name__ == "__main__":
    main()
