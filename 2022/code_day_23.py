import sys
from pathlib import Path
from collections import defaultdict

sys.path.append(str(Path(__file__).parent.parent))
import import_data

def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    data = preprocess(data)
    return data


def preprocess(data):
    grid = set()
    for row_idx, row in enumerate(data):
        for col_idx, val in enumerate(row):
            if val == '#':
                grid.add((row_idx, col_idx))
    return grid


def take_step(grid, step):
    # step is offset for directions
    DIRECTIONS = {
        'N': ((-1, -1), (-1, 0), (-1, 1)),
        'S': ((1, -1), (1, 0), (1, 1)),
        'W': ((-1, -1), (0, -1), (1, -1)),
        'E': ((-1, 1), (0, 1), (1, 1))
    }
    directions_rotation = 'NSWE'
    new_grid = defaultdict(list)
    for elf in grid:
        if has_neighbours(elf, grid):
            row_idx, col_idx = elf
            #move
            for step_offset in range(4):
                directions_index = (step + step_offset) % 4
                test_directions = DIRECTIONS[directions_rotation[directions_index]]
                for row_diff, col_diff in test_directions:
                    test_elf = row_idx + row_diff, col_idx + col_diff
                    if test_elf in grid:
                        break
                else:
                    row_diff, col_diff = test_directions[1]
                    new_elf = row_idx + row_diff, col_idx + col_diff
                    new_grid[new_elf].append(elf)
                    break
            else:
                new_grid[elf].append(elf)
        else:
            new_grid[elf].append(elf)
    # check for duplicates
    final_grid = set()
    moved = False
    for new_location, old_locations in new_grid.items():
        if len(old_locations) == 1:
            if old_locations[0] != new_location:
                moved = True
            final_grid.add(new_location)
        else:
            for location in old_locations:
                final_grid.add(location)
    assert len(final_grid) == len(grid)
    return final_grid, moved


def has_neighbours(elf, grid):
    NEIGHBOURS = (
        (-1, -1), (-1,  0), (-1,  1),
        ( 0, -1),           ( 0,  1),
        ( 1, -1), ( 1,  0), ( 1,  1)
    )
    row_idx, col_idx = elf
    for row_diff, col_diff in NEIGHBOURS:
        test_elf = row_idx + row_diff, col_idx + col_diff
        if test_elf in grid:
            return True
    return False


def get_area(grid):
    min_coords = [min(coords[idx] for coords in grid) for idx in range(2)]
    max_coords = [max(coords[idx] for coords in grid) for idx in range(2)]
    return (max_coords[0] - min_coords[0] + 1) * (max_coords[1] - min_coords[1] + 1) - len(grid)


def part_1(data):
    for step in range(10):
        data, _ = take_step(data, step)
    return get_area(data)


def part_2(data):
    moved = True
    step = 0
    while moved:
        data, moved = take_step(data, step)
        step += 1
    return step


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
