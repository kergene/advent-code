def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum.split(',')


def closest_crossing(data):
    cells = [set(), set()]
    for index, wire in enumerate(data):
        r, c = 0, 0
        for command in wire:
            direction = command[0]
            distance = int(command[1:])
            if direction == 'R':
                for _ in range(distance):
                    c += 1
                    cells[index].add((r, c))
            elif direction == 'L':
                for _ in range(distance):
                    c -= 1
                    cells[index].add((r, c))
            elif direction == 'U':
                for _ in range(distance):
                    r += 1
                    cells[index].add((r, c))
            elif direction == 'D':
                for _ in range(distance):
                    r -= 1
                    cells[index].add((r, c))
            else:
                assert False
    crossings = cells[0].intersection(cells[1])
    return min(abs(x[0]) + abs(x[1]) for x in crossings)


def fewest_steps(data):
    cells = [{}, {}]
    for index, wire in enumerate(data):
        r, c = 0, 0
        d = 0
        for command in wire:
            direction = command[0]
            distance = int(command[1:])
            if direction == 'R':
                for _ in range(distance):
                    c += 1
                    d += 1
                    if (r, c) not in cells[index]:
                        cells[index][(r, c)] = d
            elif direction == 'L':
                for _ in range(distance):
                    c -= 1
                    d += 1
                    if (r, c) not in cells[index]:
                        cells[index][(r, c)] = d
            elif direction == 'U':
                for _ in range(distance):
                    r += 1
                    d += 1
                    if (r, c) not in cells[index]:
                        cells[index][(r, c)] = d
            elif direction == 'D':
                for _ in range(distance):
                    r -= 1
                    d += 1
                    if (r, c) not in cells[index]:
                        cells[index][(r, c)] = d
            else:
                assert False
    crossings = set(cells[0].keys()).intersection(set(cells[1].keys()))
    return min(abs(cells[0][x]) + abs(cells[1][x]) for x in crossings)


def main():
    year, day = 2019, 3
    data = get_data(year, day)
    print(closest_crossing(data))
    print(fewest_steps(data))


if __name__ == "__main__":
    main()
