from itertools import product


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def set_display(data):
    grid = [[0 for _ in range(50)] for _ in range(6)]
    for line in data:
        line = line.split()
        if line[0] == 'rect':
            x, y = line[1].split('x')
            for i, j in product(range(int(x)), range(int(y))):
                grid[j][i] = 1
        else:
            # rotate
            if line[1] == 'row':
                index = int(line[2].split('=')[-1])
                amount = int(line[-1])
                rotator = grid[index].copy()
                for i in range(50):
                    grid[index][(i + amount) % 50] = rotator[i]
            else:
                # column
                index = int(line[2].split('=')[-1])
                amount = int(line[-1])
                rotator = [row[index] for row in grid].copy()
                for i in range(6):
                    grid[(i + amount) % 6][index] = rotator[i]
    return sum(sum(row) for row in grid), grid


def view_display(grid):
    strings = []
    for row in grid:
        substrings = []
        for cell in row:
            if cell == 1:
                substrings.append('||')
            else:
                substrings.append('  ')
        strings.append(''.join(substrings))
    return '\n'.join(strings)


def main():
    year, day = 2016, 8
    data = get_data(year, day)
    on_count, grid = set_display(data)
    print(on_count)
    print(view_display(grid))


if __name__ == "__main__":
    main()
