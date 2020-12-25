DIRECTIONS = ((-1,-1), (-1, 0), (-1, 1),
              ( 0,-1),          ( 0, 1), 
              ( 1,-1), ( 1, 0), ( 1, 1)
             )


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [list(datum) for datum in data]
    return data


def flip_lights(data):
    n_row = len(data)
    n_col = len(data[0])
    for _ in range(100):
        data = take_step(data, n_row, n_col)
    return sum(1 for row in data for i in row if i == '#')


def take_step(data, n_row, n_col):
    return [[update_cell(x, y, data, n_row, n_col) for y in range(n_col)] for x in range(n_row)]


def update_cell(x, y, data, n_row, n_col):
    ons = 0
    for dx, dy in DIRECTIONS:
        a, b = x+dx, y+dy
        if 0 <= a < n_row and 0 <= b < n_col:
            if data[a][b] == '#':
                ons += 1
    if data[x][y] == '#':
        if ons == 2 or ons == 3:
            return '#'
        else:
            return '.'
    elif data[x][y] == '.':
        if ons == 3:
            return '#'
        else:
            return '.'


def fixed_corners(data):
    n_row = len(data)
    n_col = len(data[0])
    for _ in range(100):
        data = take_step_fixed_corners(data, n_row, n_col)
    return sum(1 for row in data for i in row if i == '#')


def take_step_fixed_corners(data, n_row, n_col):
    data = [[update_cell(x, y, data, n_row, n_col) for y in range(n_col)] for x in range(n_row)]
    data[0][0] = '#'
    data[0][-1] = '#'
    data[-1][0] = '#'
    data[-1][-1] = '#'
    return data


def main():
    year, day = 2015, 18
    data = get_data(year, day)
    print(flip_lights(data))
    print(fixed_corners(data))


if __name__ == "__main__":
    main()
