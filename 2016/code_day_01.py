def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(', ')
    return data


def follow_directions(data):
    x = 0
    y = 0
    MOVE = ((-1, 0), (0, -1), (1, 0), (0, 1))
    choice = 2
    for line in data:
        direction = line[0]
        size = int(line[1:])
        if direction == 'L':
            choice += 1
        else:
            choice -= 1
        x += MOVE[choice % 4][0] * size
        y += MOVE[choice % 4][1] * size
    return abs(x) + abs(y)


def first_crossing(data):
    x = 0
    y = 0
    MOVE = ((-1, 0), (0, -1), (1, 0), (0, 1))
    choice = 2
    seen = set()
    seen.add((x,y))
    for line in data:
        direction = line[0]
        size = int(line[1:])
        if direction == 'L':
            choice += 1
        else:
            choice -= 1
        for _ in range(size):
            x += MOVE[choice % 4][0]
            y += MOVE[choice % 4][1]
            if ((x,y)) in seen:
                return abs(x) + abs(y)
            else:
                seen.add((x,y))


def main():
    year, day = 2016, 1
    data = get_data(year, day)
    print(follow_directions(data))
    print(first_crossing(data))


if __name__ == "__main__":
    main()
