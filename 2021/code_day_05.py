from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return tuple(tuple(int(val) for val in xy.split(',')) for xy in datum.split(' -> '))


def count_intersections(data):
    coords = defaultdict(int)
    for row in data:
        one, two = row
        x1, y1 = one
        x2, y2 = two
        if x1 == x2:
            y1, y2 = min(y1, y2), max(y1, y2)
            for y in range(y1, y2+1):
                coords[(x1, y)] += 1
        elif y1 == y2:
            x1, x2 = min(x1, x2), max(x1, x2)
            for x in range(x1, x2+1):
                coords[(x, y1)] += 1
    return sum(val > 1 for val in coords.values())


def count_intersections_with_diagonals(data):
    coords = defaultdict(int)
    for row in data:
        one, two = row
        x1, y1 = one
        x2, y2 = two
        if x1 == x2:
            y1, y2 = min(y1, y2), max(y1, y2)
            for y in range(y1, y2+1):
                coords[(x1, y)] += 1
        elif y1 == y2:
            x1, x2 = min(x1, x2), max(x1, x2)
            for x in range(x1, x2+1):
                coords[(x, y1)] += 1
        else:
            xdiff = 1 if x2 > x1 else -1
            ydiff = 1 if y2 > y1 else -1
            for offset in range(abs(x1 - x2) + 1):
                coords[(x1 + offset*xdiff, y1 + offset*ydiff)] += 1
    return sum(val > 1 for val in coords.values())


def main():
    year, day = 2021, 5
    data = get_data(year, day)
    print(count_intersections(data))
    print(count_intersections_with_diagonals(data))


if __name__ == "__main__":
    main()
