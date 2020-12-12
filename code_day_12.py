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
    for i,j in data:
        if i == 'N':
            y += j
        elif i == 'S':
            y -= j
        elif i == 'E':
            x += j
        elif i == 'W':
            x -= j
        elif i == 'F':
            x += DIRS[dirs_idx][0] * j
            y += DIRS[dirs_idx][1] * j
        elif i == 'R':
            dirs_idx += (j // 90)
            dirs_idx = dirs_idx % 4
        elif i == 'L':
            dirs_idx -= (j // 90)
            dirs_idx = dirs_idx % 4
    return abs(x) + abs(y)

def waypoint_relocate(data):
    x_way = 10
    y_way = 1
    x = 0
    y = 0
    for i,j in data:
        if i == 'N':
            y_way += j
        elif i == 'S':
            y_way -= j
        elif i == 'E':
            x_way += j
        elif i == 'W':
            x_way -= j
        elif i == 'F':
            x += j * x_way
            y += j * y_way
        elif i == 'R':
            for _ in range((j // 90) % 4):
                x_way, y_way = y_way, -x_way
        elif i == 'L':
            for _ in range((j // 90) % 4):
                x_way, y_way = -y_way, x_way
    return abs(x) + abs(y)

def main():
    day = 12
    data = get_data(day)
    print(relocate(data))
    print(waypoint_relocate(data))

if __name__ == "__main__":
    main()
