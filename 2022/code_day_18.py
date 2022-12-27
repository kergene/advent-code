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
    return tuple(int(val) for val in datum.split(','))


def part_1(data):
    DIRECTIONS = (
        (1,0,0), (-1,0,0),
        (0,1,0), (0,-1,0),
        (0,0,1), (0,0,-1)
    )
    data = set(data)
    total = 6 * len(data)
    for coord_x, coord_y, coord_z in data:
        for diff_x, diff_y, diff_z in DIRECTIONS:
            if (coord_x + diff_x, coord_y + diff_y, coord_z + diff_z) in data:
                total -= 1
    return total


def part_2(data):
    DIRECTIONS = (
        (1,0,0), (-1,0,0),
        (0,1,0), (0,-1,0),
        (0,0,1), (0,0,-1)
    )
    data = set(data)
    lowers = tuple(min(x) - 1 for x in zip(*data))
    uppers = tuple(max(x) + 1 for x in zip(*data))
    total = 0
    seens = set()
    queue = set()
    queue.add(lowers)
    while queue:
        choice = coord_x, coord_y, coord_z = queue.pop()
        seens.add(choice)
        for diff_x, diff_y, diff_z in DIRECTIONS:
            new_choice = coord_x + diff_x, coord_y + diff_y, coord_z + diff_z
            if all(lowers[idx] <= new_choice[idx] <= uppers[idx] for idx in range(3)):
                if new_choice not in seens and new_choice not in data:
                    queue.add(new_choice)
                if new_choice in data:
                    total += 1
    return total


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(data)
    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
