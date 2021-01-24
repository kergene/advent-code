def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    data = [preprocess(datum) for datum in data.split(',')]
    return data


def preprocess(datum):
    return datum


def distance(x, y, z):
 return (abs(x) + abs(y) + abs(z)) // 2


def final_distance(data):
    x = y = z = 0
    for direction in data:
        if direction == 'n':
            y += 1
            z -= 1
        elif direction == 's':
            y -= 1
            z += 1
        elif direction == 'ne':
            x += 1
            z -= 1
        elif direction == 'sw':
            x -= 1
            z += 1
        elif direction == 'nw':
            y += 1
            x -= 1
        elif direction == 'se':
            y -= 1
            x += 1
        else:
            assert False
    return distance(x, y, z)


def max_distance(data):
    x = y = z = 0
    max_dist = 0
    for direction in data:
        if direction == 'n':
            y += 1
            z -= 1
        elif direction == 's':
            y -= 1
            z += 1
        elif direction == 'ne':
            x += 1
            z -= 1
        elif direction == 'sw':
            x -= 1
            z += 1
        elif direction == 'nw':
            y += 1
            x -= 1
        elif direction == 'se':
            y -= 1
            x += 1
        else:
            assert False
        max_dist = max(distance(x, y, z), max_dist)
    return max_dist


def main():
    year, day = 2017, 11
    data = get_data(year, day)
    print(final_distance(data))
    print(max_distance(data))


if __name__ == "__main__":
    main()
