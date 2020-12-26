def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def get_key(data):
    result = []
    for line in data:
        x = y = 1
        for letter in line:
            if letter == 'U':
                if x > 0:
                    x -= 1
            elif letter == 'D':
                if x < 2:
                    x += 1
            elif letter == 'L':
                if y > 0:
                    y -= 1
            elif letter == 'R':
                if y < 2:
                    y += 1
        result.append(str(3*x + y + 1))
    return ''.join(result)


def get_key_plus(data):
    grid = [['0','0','1','0','0'],
            ['0','2','3','4','0'],
            ['5','6','7','8','9'],
            ['0','A','B','C','0'],
            ['0','0','D','0','0']]
    result = []
    for line in data:
        x, y = 2, 0
        for letter in line:
            if letter == 'U':
                if x > 0:
                    if grid[x-1][y] != '0':
                        x -= 1
            elif letter == 'D':
                if x < 4:
                    if grid[x+1][y] != '0':
                        x += 1
            elif letter == 'L':
                if y > 0:
                    if grid[x][y-1] != '0':
                        y -= 1
            elif letter == 'R':
                if y < 4:
                    if grid[x][y+1] != '0':
                        y += 1
        result.append(grid[x][y])
    return ''.join(result)


def main():
    year, day = 2016, 2
    data = get_data(year, day)
    print(get_key(data))
    print(get_key_plus(data))


if __name__ == "__main__":
    main()
