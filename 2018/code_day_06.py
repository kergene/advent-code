from math import ceil
from collections import Counter


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return tuple(int(part.strip()) for part in datum.split(','))


def non_inf_area(data):
    min_x = min(x[0] for x in data)
    min_y = min(x[1] for x in data)
    max_x = max(x[0] for x in data)
    max_y = max(x[1] for x in data)
    x_range = max_x - min_x
    y_range = max_y - min_y
    grid = dict()
    infinite = set()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            min_distance = 2 * (x_range + y_range)
            for idx, centre in enumerate(data):
                dist = manhattan_distance((x, y), centre)
                if dist < min_distance:
                    min_distance = dist
                    closest = idx
                elif dist == min_distance:
                    closest = -1
            grid[x,y] = closest
            if x in (min_x, max_x) or y in (min_y, max_y):
                infinite.add(closest)
    c = Counter(grid.values())
    for key, value in c.most_common():
        if key not in infinite and key != -1:
            return value


def manhattan_distance(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


def close_points(data):
    max_dist = 10000
    max_extension = ceil(max_dist / len(data))
    min_x = min(x[0] for x in data)
    min_y = min(x[1] for x in data)
    max_x = max(x[0] for x in data)
    max_y = max(x[1] for x in data)
    min_x -= max_extension
    max_x += max_extension
    min_y -= max_extension
    max_y += max_extension
    count = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            total = 0
            for centre in data:
                total += manhattan_distance((x, y), centre)
                if total >= max_dist:
                    break
            if total < max_dist:
                count += 1
    return count


def main():
    year, day = 2018, 6
    data = get_data(year, day)
    print(non_inf_area(data))
    print(close_points(data))


if __name__ == "__main__":
    main()
