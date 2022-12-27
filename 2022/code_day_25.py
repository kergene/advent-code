import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import import_data

def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    return data


def part_1(data):
    total = 0
    for row in data:
        total += snafu_to_decimal(row)
    return decimal_to_snafu(total)


def snafu_to_decimal(snafu):
    decimal = 0
    for character in snafu:
        decimal *= 5
        if character in '012':
            decimal += int(character)
        elif character == '=':
            decimal -= 2
        elif character == '-':
            decimal -= 1
    return decimal


def decimal_to_snafu(decimal):
    snafu_stack = []
    while decimal != 0:
        if decimal % 5 in (0, 1, 2):
            snafu_stack.append(str(decimal % 5))
            decimal -= (decimal % 5)
        elif decimal % 5 == 3:
            snafu_stack.append('=')
            decimal += 2
        elif decimal % 5 == 4:
            snafu_stack.append('-')
            decimal += 1
        decimal //= 5
    return ''.join(reversed(snafu_stack))

def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(part_1(data))


if __name__ == "__main__":
    main()
