def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data

def preprocess(datum):
    return datum[0], int(datum[1:])

def relocate(data):
    x = 0
    y = 0
    DIRS = ((1,0), (0, -1), (-1, 0), (0, 1))
    dirs_idx = 0
    for command, size in data:
        if command == 'N':
            y += size
        elif command == 'S':
            y -= size
        elif command == 'E':
            x += size
        elif command == 'W':
            x -= size
        elif command == 'F':
            x += DIRS[dirs_idx][0] * size
            y += DIRS[dirs_idx][1] * size
        elif command == 'R':
            dirs_idx += (size // 90)
            dirs_idx = dirs_idx % 4
        elif command == 'L':
            dirs_idx -= (size // 90)
            dirs_idx = dirs_idx % 4
    return abs(x) + abs(y)

def waypoint_relocate(data):
    x_way = 10
    y_way = 1
    x = 0
    y = 0
    for command, size in data:
        if command == 'N':
            y_way += size
        elif command == 'S':
            y_way -= size
        elif command == 'E':
            x_way += size
        elif command == 'W':
            x_way -= size
        elif command == 'F':
            x += size * x_way
            y += size * y_way
        elif command == 'R':
            for _ in range((size // 90) % 4):
                x_way, y_way = y_way, -x_way
        elif command == 'L':
            for _ in range((size // 90) % 4):
                x_way, y_way = -y_way, x_way
    return abs(x) + abs(y)

def main():
    day = 12
    data = get_data(day)
    print(relocate(data))
    print(waypoint_relocate(data))

if __name__ == "__main__":
    main()
