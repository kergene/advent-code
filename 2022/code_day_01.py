import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import import_data


def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().split('\n\n')
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return [int(val) for val in datum.split()]


def count_calories(data, num_to_sum):
    data = sorted(sum(vals) for vals in data)
    return sum(data[-num_to_sum:])


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(count_calories(data, 1))
    print(count_calories(data, 3))


if __name__ == "__main__":
    main()
