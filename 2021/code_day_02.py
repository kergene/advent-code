def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum.split()


def find_course(data):
    horizontal = 0
    vertical = 0
    for row in data:
        direction = row[0]
        amount = int(row[1])
        if direction == 'up':
            vertical -= amount
        elif direction == 'down':
            vertical += amount
        elif direction == 'forward':
            horizontal += amount
        else:
            assert False
    return horizontal * vertical


def find_aim(data):
    horizontal = 0
    vertical = 0
    aim = 0
    for row in data:
        direction = row[0]
        amount = int(row[1])
        if direction == 'up':
            aim -= amount
        elif direction == 'down':
            aim += amount
        elif direction == 'forward':
            horizontal += amount
            vertical += amount * aim
        else:
            assert False
    return horizontal * vertical


def main():
    year, day = 2021, 2
    data = get_data(year, day)
    print(find_course(data))
    print(find_aim(data))


if __name__ == "__main__":
    main()
