import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import import_data

def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    movement_dir, val = datum.split()
    return movement_dir, int(val)


def sign(x):
    return (x > 0) - (x < 0)


def tail_locations(data, rope_length):
    positions = set()
    directions = {
        'L': (-1, 0),
        'R': (1, 0),
        'D': (0, -1),
        'U': (0, 1)
    }
    coords_x = [0] * rope_length
    coords_y = [0] * rope_length
    positions.add((coords_x[-1], coords_y[-1]))
    for row in data:
        movement_dir, val = row
        coords_x_diff, coords_y_diff = directions[movement_dir]
        for _ in range(val):
            coords_x[0] += coords_x_diff
            coords_y[0] += coords_y_diff
            updated = True
            while updated:
                coords_x, coords_y, updated = update_tail(coords_x, coords_y)
            positions.add((coords_x[-1], coords_y[-1]))
    return len(positions)


def update_tail(coords_x, coords_y):
    updated = False
    for idx in range(1, len(coords_x)):
        if abs(coords_x[idx - 1] - coords_x[idx]) > 1 or abs(coords_y[idx - 1] - coords_y[idx]) > 1:
            updated = True
            move_dir_x = sign(coords_x[idx - 1] - coords_x[idx])
            move_dir_y = sign(coords_y[idx - 1] - coords_y[idx])
            coords_x[idx] += move_dir_x
            coords_y[idx] += move_dir_y
            return coords_x, coords_y, updated
    return coords_x, coords_y, updated


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(tail_locations(data, 2))
    print(tail_locations(data, 10))


if __name__ == "__main__":
    main()
