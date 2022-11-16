from math import ceil
from math import floor


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(': ')[1]
    data = data.split(", ")
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = datum.split('=')[1]
    return tuple(int(val) for val in datum.split('..'))


def probe_height(data):
    x_min, x_max = data[0]
    y_min, y_max = data[1]
    min_dx = ceil((2*x_min) ** 0.5)
    max_dx = x_max
    high_y = y_max
    for init_dx in range(min_dx, max_dx + 1):
        dx = init_dx
        x = 0
        n = 0
        while x <= x_max and dx != 0:
            x += dx
            dx -= 1
            n += 1
            if x_min <= x <= x_max:
                min_dy = ceil((n - 1)/2 + y_min/n)
                max_dy = floor((n - 1)/2 + y_max/n)
                if min_dy <= max_dy:
                    max_y = max_dy*(max_dy + 1)//2
                    if max_y > high_y:
                        high_y = max_y
        if dx == 0:
            n_min = n
            for n in range(n_min, -y_min*2 + 1):
                min_dy = ceil((n - 1)/2 + y_min/n)
                max_dy = floor((n - 1)/2 + y_max/n)
                if min_dy <= max_dy:
                    max_y = max_dy*(max_dy + 1)//2
                    if max_y > high_y:
                        high_y = max_y
    return high_y


def count_velocities(data):
    x_min, x_max = data[0]
    y_min, y_max = data[1]
    min_dx = floor((2*x_min) ** 0.5)
    max_dx = x_max
    solutions = set()
    for init_dx in range(min_dx, max_dx + 1):
        dx = init_dx
        x = 0
        n = 0
        while x <= x_max and dx != 0:
            x += dx
            dx -= 1
            n += 1
            if x_min <= x <= x_max:
                min_dy = ceil((n - 1)/2 + y_min/n)
                max_dy = floor((n - 1)/2 + y_max/n)
                if min_dy <= max_dy:
                    for init_dy in range(min_dy, max_dy + 1):
                        solutions.add((init_dx, init_dy))
        if dx == 0 and x >= x_min:
            n_min = n
            for n in range(n_min, -y_min*2 + 1):
                min_dy = ceil((n - 1)/2 + y_min/n)
                max_dy = floor((n - 1)/2 + y_max/n)
                if min_dy <= max_dy:
                    for init_dy in range(min_dy, max_dy + 1):
                        solutions.add((init_dx, init_dy))
    return len(solutions)


def main():
    year, day = 2021, 17
    data = get_data(year, day)
    print(probe_height(data))
    print(count_velocities(data))


if __name__ == "__main__":
    main()
