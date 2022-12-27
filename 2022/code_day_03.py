import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import import_data

def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    return data


def mispacking(data):
    total = 0
    for row in data:
        l = len(row) // 2
        unique = set(row[:l]).intersection(row[l:]).pop()
        total += get_priority(unique)
    return total


def get_priority(unique):
    x = ord(unique)
    if x >= ord('a'):
        x -= ord('a') - 1
    else:
        x -= ord('A') - 27
    return x


def badging(data):
    total = 0
    for idx in range(len(data) // 3):
        split_range = data[idx*3:idx*3+3]
        unique = set(split_range[0]).intersection(split_range[1]).intersection(split_range[2]).pop()
        total += get_priority(unique)
    return total


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(mispacking(data))
    print(badging(data))


if __name__ == "__main__":
    main()
