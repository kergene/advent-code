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
    datum = datum.split(',')
    datum = [[int(val) for val in elf.split('-')] for elf in datum]
    return datum


def full_overlaps(data):
    total = 0
    for row in data:
        id1, id2 = row
        if id1[0] >= id2[0] and id1[1] <= id2[1]:
            total += 1
        elif id1[0] <= id2[0] and id1[1] >= id2[1]:
            total += 1
    return total


def any_overlaps(data):
    total = 0
    for row in data:
        id1, id2 = row
        if id1[0] <= id2[1] and id1[1] >= id2[0]:
            total += 1
    return total


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(full_overlaps(data))
    print(any_overlaps(data))


if __name__ == "__main__":
    main()
