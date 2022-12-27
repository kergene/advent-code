import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import import_data

def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().split('\n\n')
    grid = data[0].splitlines()
    grid = process_grid(grid)
    moves = data[1].replace('L', ' L ').replace('R', ' R ').split()
    moves = [preprocess(move) for move in moves]
    return grid, moves


def process_grid(grid):
    grid_dict = {}
    for row_coord, row in enumerate(grid):
        for col_coord, val in enumerate(row):
            if val == '.':
                grid_dict[row_coord, col_coord] = '.'
            elif val == '#':
                grid_dict[row_coord, col_coord] = '#'
    return grid_dict


def preprocess(datum):
    if datum in 'LR':
        return datum
    return int(datum)


def part_1(data):
    grid, moves = data
    DIRECTIONS = {
        'R': (0, 1),
        'D': (1, 0),
        'L': (0, -1),
        'U': (-1, 0)
    }
    direction_rotation = 'RDLU'
    boundaries = get_boundaries(grid)
    row_coord = 0
    row = [coords for coords in grid.keys() if coords[0] == row_coord]
    col_coord = min(coords[1] for coords in row)
    direction_idx = 0
    for row in moves:
        if row == 'L':
            direction_idx -= 1
            direction_idx %= 4
        elif row == 'R':
            direction_idx += 1
            direction_idx %= 4
        else:
            # move forwards
            direction = direction_rotation[direction_idx]
            row_diff, col_diff = DIRECTIONS[direction]
            for _ in range(row):
                new_row = row_coord + row_diff
                new_col = col_coord + col_diff
                if (new_row, new_col) in grid:
                    if grid[new_row, new_col] == '.':
                        row_coord = new_row
                        col_coord = new_col
                    else:
                        break
                else:
                    if direction in 'LR':
                        # look for row coord, return col coord
                        new_col = boundaries[direction, row_coord]
                        if grid[row_coord, new_col] == '.':
                            col_coord = new_col
                        else:
                            break
                    else:
                        new_row = boundaries[direction, col_coord]
                        if grid[new_row, col_coord] == '.':
                            row_coord = new_row
                        else:
                            break
    return (row_coord + 1) * 1000 + (col_coord + 1) * 4 + direction_idx

# 157102 too low
# 158106 too low


def get_boundaries(grid):
    boundaries = {}
    max_row = max(coords[0] for coords in grid.keys())
    max_col = max(coords[1] for coords in grid.keys())
    # iterate over rows, leftmost is 
    for row_coord in range(max_row + 1):
        row = [coords for coords in grid.keys() if coords[0] == row_coord]
        boundaries['R', row_coord] = min(coords[1] for coords in row)
        boundaries['L', row_coord] = max(coords[1] for coords in row)
    for col_coord in range(max_col + 1):
        col = [coords for coords in grid.keys() if coords[1] == col_coord]
        boundaries['D', col_coord] = min(coords[0] for coords in col)
        boundaries['U', col_coord] = max(coords[0] for coords in col)
    return boundaries


def get_boundaries_cube():
    # nets are 50x50
    # we just hardcode all 14 sides for our input
    boundaries = {}
    for row_coord in range(0, 50):
        # left moves to (149...100), 0, R
        boundaries['L', row_coord] = 149 - row_coord, 0, 'R'
        # right moves to (149...100), 99, L
        boundaries['R', row_coord] = 149 - row_coord, 99, 'L'
    for row_coord in range(50, 100):
        # left moves to 100, (0...49), D
        boundaries['L', row_coord] = 100, row_coord - 50, 'D'
        # right moves to 49, (100...149), U
        boundaries['R', row_coord] = 49, row_coord + 50, 'U'
    for row_coord in range(100, 150):
        # left moves to (49...0), 50, R
        boundaries['L', row_coord] = 149 - row_coord, 50, 'R'
        # right moves to (49...0), 149, L
        boundaries['R', row_coord] = 149 - row_coord, 149, 'L'
    for row_coord in range(150, 200):
        # left moves to 0, 50...99, D
        boundaries['L', row_coord] = 0, row_coord - 100, 'D'
        # right moves to 149, 50...99, U
        boundaries['R', row_coord] = 149, row_coord - 100, 'U'
    for col_coord in range(0, 50):
        # up moves to 50...99, 50, R
        boundaries['U', col_coord] = col_coord + 50, 50, 'R'
        # down moves to 0, 100...149, D
        boundaries['D', col_coord] = 0, col_coord + 100, 'D'
    for col_coord in range(50, 100):
        # up moves to 150...199, 0, R
        boundaries['U', col_coord] = col_coord + 100, 0, 'R'
        # down moves to 150...199, 49, L
        boundaries['D', col_coord] = col_coord + 100, 49, 'L'
    for col_coord in range(100, 150):
        # up moves to 199, 0...49, U
        boundaries['U', col_coord] = 199, col_coord - 100, 'U'
        # down moves to 50...99, 99, L
        boundaries['D', col_coord] = col_coord - 50, 99, 'L'
    return boundaries


def part_2(data):
    grid, moves = data
    DIRECTIONS = {
        'R': (0, 1),
        'D': (1, 0),
        'L': (0, -1),
        'U': (-1, 0)
    }
    direction_rotation = 'RDLU'
    boundaries = get_boundaries_cube()
    row_coord = 0
    row = [coords for coords in grid.keys() if coords[0] == row_coord]
    col_coord = min(coords[1] for coords in row)
    direction_idx = 0
    for row in moves:
        if row == 'L':
            direction_idx -= 1
            direction_idx %= 4
        elif row == 'R':
            direction_idx += 1
            direction_idx %= 4
        else:
            # move forwards
            direction = direction_rotation[direction_idx]
            row_diff, col_diff = DIRECTIONS[direction]
            for _ in range(row):
                new_row = row_coord + row_diff
                new_col = col_coord + col_diff
                if (new_row, new_col) in grid:
                    if grid[new_row, new_col] == '.':
                        row_coord = new_row
                        col_coord = new_col
                    else:
                        break
                else:
                    if direction in 'LR':
                        # look for row coord, return col coord
                        new_row, new_col, new_dir = boundaries[direction, row_coord]
                        if grid[new_row, new_col] == '.':
                            row_coord = new_row
                            col_coord = new_col
                            direction_idx = direction_rotation.index(new_dir)
                            direction = direction_rotation[direction_idx]
                            row_diff, col_diff = DIRECTIONS[direction]
                        else:
                            break
                    else:
                        new_row, new_col, new_dir = boundaries[direction, col_coord]
                        if grid[new_row, new_col] == '.':
                            row_coord = new_row
                            col_coord = new_col
                            direction_idx = direction_rotation.index(new_dir)
                            direction = direction_rotation[direction_idx]
                            row_diff, col_diff = DIRECTIONS[direction]
                        else:
                            break
    return (row_coord + 1) * 1000 + (col_coord + 1) * 4 + direction_idx


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
