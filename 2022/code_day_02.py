import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import import_data


def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    return data


def double_rps(data):
    total = 0
    for row in data:
        theirs = ord(row[0]) - 65
        mine = ord(row[2]) - 88
        total += mine + 1
        total += 3 * ((mine - theirs + 1) % 3)
    return total


def rps_win(data):
    total = 0
    for row in data:
        theirs = ord(row[0]) - 65
        win = ord(row[2]) - 88
        total += (theirs + win - 1) % 3 + 1
        total += 3*win
    return total


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(double_rps(data))
    print(rps_win(data))


if __name__ == "__main__":
    main()
