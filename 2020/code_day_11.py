DIRECTIONS = (
    (-1,-1),(-1,0),(-1,1),
    (0,-1),        (0,1),
    (1,-1), (1,0), (1,1)
)


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [[element for element in row] for row in data]
    return data


def test_equality(data, new_data, n):
    for i in range(n):
        if new_data[i] != data[i]:
            return False
    return True


def find_stability(data):
    n = len(data)
    m = len(data[0])
    stable = False
    while not stable:
        new_data = take_step(data, n, m)
        stable = test_equality(data, new_data, n)
        data = new_data
    return sum(1 for row in data for element in row if element == '#')


def take_step(data, n, m):
    return [[replace_seat(x, y, data, n, m) for y in range(m)] for x in range(n)]


def replace_seat(x, y, data, n, m):
    if data[x][y] == 'L':
        for dx, dy in DIRECTIONS:
            a,b = x+dx,y+dy
            if 0 <= a < n and 0 <= b < m:
                if data[a][b] == '#':
                    return 'L'
        return '#'
    elif data[x][y] == '#':
        fulls = 0
        for dx, dy in DIRECTIONS:
            a,b = x+dx,y+dy
            if 0 <= a < n and 0 <= b < m:
                if data[a][b] == '#':
                    fulls += 1
                    if fulls >= 4:
                        return 'L'
        return '#'
    else:
        return data[x][y]


def find_stability_long_see(data):
    n = len(data)
    m = len(data[0])
    stable = False
    while not stable:
        new_data = take_step_long(data, n, m)
        stable = test_equality(data, new_data, n)
        data = new_data
    return sum(1 for row in data for element in row if element == '#')


def take_step_long(data, n, m):
    return [[replace_seat_long(x, y, data, n, m) for y in range(m)] for x in range(n)]


def replace_seat_long(x, y, data, n, m):
    if data[x][y] == 'L':
        for dx, dy in DIRECTIONS:
            a,b=x,y
            seat = False
            while not seat:
                seat = True
                a,b = a+dx,b+dy
                if 0 <= a < n and 0 <= b < m:
                    if data[a][b] == '.':
                        seat = False
                    elif data[a][b] == '#':
                        return 'L'
        return '#'
    elif data[x][y] == '#':
        fulls = 0
        for dx, dy in DIRECTIONS:
            a,b=x,y
            seat = False
            while not seat:
                seat = True
                a,b = a+dx,b+dy
                if 0 <= a < n and 0 <= b < m:
                    if data[a][b] == '.':
                        seat = False
                    elif data[a][b] == '#':
                        fulls += 1
                        if fulls >= 5:
                            return 'L'
        return '#'
    else:
        return data[x][y]


def main():
    year, day = 2020, 11
    data = get_data(year, day)
    print(find_stability(data))
    print(find_stability_long_see(data))


if __name__ == "__main__":
    main()
