def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return int(data)


def best_power_3(serial_no):
    grid = [[0 for _ in range(1, 301)] for _ in range(1, 301)]
    for x in range(1, 301):
        rack_id = x + 10
        for y in range(1, 301):
            power = rack_id * y
            power += serial_no
            power *= rack_id
            power = int(str(power)[-3])
            power -= 5
            grid[y - 1][x - 1] = power
    max_pow = min(min(row) for row in grid) * 9
    sums = []
    for y in range(300):
        row_sums = []
        row_sums.append(sum(grid[y][:3]))
        for x in range(300 - 3):
            row_sums.append(row_sums[-1] - grid[y][x] + grid[y][x + 3])
        sums.append(row_sums)
    sums = list(zip(*sums))
    for x in range(len(sums)):
        row = sums[x]
        row_sum = sum(row[:3])
        if row_sum > max_pow:
            max_pow = row_sum
            coords = str(x + 1) + ',' + str(1)
        for y in range(300 - 3):
            row_sum += row[y + 3] - row[y]
            if row_sum > max_pow:
                max_pow = row_sum
                coords = str(x + 1) + ',' + str(y + 2)
    return coords


def best_power_all(serial_no):
    grid = [[0 for _ in range(1, 301)] for _ in range(1, 301)]
    for x in range(1, 301):
        rack_id = x + 10
        for y in range(1, 301):
            power = rack_id * y
            power += serial_no
            power *= rack_id
            power = int(str(power)[-3])
            power -= 5
            grid[y - 1][x - 1] = power
    max_pow = min(min(row) for row in grid)
    for size in range(1,301):
        sums = []
        for y in range(300):
            row_sums = []
            row_sums.append(sum(grid[y][:size]))
            for x in range(300 - size):
                row_sums.append(row_sums[-1] - grid[y][x] + grid[y][x + size])
            sums.append(row_sums)
        sums = list(zip(*sums))
        for x in range(len(sums)):
            row = sums[x]
            row_sum = sum(row[:size])
            if row_sum > max_pow:
                max_pow = row_sum
                coords = str(x + 1) + ',' + str(1) + ',' + str(size)
            for y in range(300 - size):
                row_sum += row[y + size] - row[y]
                if row_sum > max_pow:
                    max_pow = row_sum
                    coords = str(x + 1) + ',' + str(y + 2) + ',' + str(size)
    return coords


def main():
    year, day = 2018, 11
    data = get_data(year, day)
    print(best_power_3(data))
    print(best_power_all(data))


if __name__ == "__main__":
    main()
