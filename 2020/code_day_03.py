from math import prod


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def count_trees(data, right, down):
    trees = 0
    col = 0
    col_length = len(data[0])
    for row in range(0, len(data), down):
        if data[row][col] == '#':
             trees += 1
        col += right
        col %= col_length
    return trees


def test_paths(data):
    collisions = []
    steps = ((1,1), (3,1), (5,1), (7,1), (1,2))
    for right, down in steps:
        collisions.append(count_trees(data, right, down))
    return collisions


def main():
    year, day = 2020, 3
    data = get_data(year, day)
    collisions = test_paths(data)
    print(collisions[1])
    print(prod(collisions))


if __name__ == "__main__":
    main()
