def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split()
    row = int(data[-3][:-1])
    col = int(data[-1][:-1])
    return row, col


def find_code(row, col):
    target = (row + col - 1) * (row + col - 2) // 2 + col
    rem = 20151125
    mult = 252533
    div = 33554393
    return (rem * pow(mult, target - 1, div)) % div


def main():
    year, day = 2015, 25
    row, col = get_data(year, day)
    print(find_code(row, col))


if __name__ == "__main__":
    main()
