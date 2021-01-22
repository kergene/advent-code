def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = datum.split('>')
    pos = datum[0][10:].split()
    x = int(pos[0][:-1])
    y = int(pos[1])
    vel = datum[1][11:].split()
    dx = int(vel[0][:-1])
    dy = int(vel[1])
    return [x, y, dx, dy]


def get_range(data, axis=0):
    min_axis = min(x[axis] for x in data)
    max_axis = max(x[axis] for x in data)
    return max_axis - min_axis


def take_step(data):
    new_data = []
    for x, y, dx, dy in data:
        new_data.append([x + dx, y + dy, dx, dy])
    return new_data


def print_grid(data):
    min_x = min(x[0] for x in data)
    max_x = max(x[0] for x in data)
    min_y = min(x[1] for x in data)
    max_y = max(x[1] for x in data)
    grid = [['  ' for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]
    for x, y, *_ in data:
        grid[y - min_y][x - min_x] = '||'
    output = []
    for row in grid:
        output.append(''.join(row))
    return '\n'.join(output)


def starry_message(data):
    x_range = get_range(data)
    t = 0
    while True:
        t += 1
        data, last_data = take_step(data), data
        x_range, last = get_range(data), x_range
        if last < x_range:
            return print_grid(last_data),  t-1


def main():
    year, day = 2018, 10
    data = get_data(year, day)
    message, appearance_time = starry_message(data)
    print(message)
    print(appearance_time)


if __name__ == "__main__":
    main()
