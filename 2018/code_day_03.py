from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = datum.split('@')[1]
    datum = datum.split(':')
    coords = datum[0].strip().split(',')
    x = int(coords[0])
    y = int(coords[1])
    deltas = datum[1].strip().split('x')
    dx = int(deltas[0])
    dy = int(deltas[1])
    return x, y, dx, dy


def overlapping_fabric(data):
    grid = defaultdict(int)
    for x, y, dx, dy in data:
        for a in range(x, x + dx):
            for b in range(y, y + dy):
                grid[a, b] += 1
    return sum(claim_count >= 2 for claim_count in grid.values())


def successful_claim(data):
    impossibles = set()
    grid = defaultdict(int)
    for claim_no, row in enumerate(data, start=1):
        x, y, dx, dy = row
        for a in range(x, x + dx):
            for b in range(y, y + dy):
                if grid[a, b] != 0:
                    impossibles.add(grid[a, b])
                    impossibles.add(claim_no)
                else:
                    grid[a, b] = claim_no
    for claim_no in range(1, len(data) + 1):
        if claim_no not in impossibles:
            return claim_no


def main():
    year, day = 2018, 3
    data = get_data(year, day)
    print(overlapping_fabric(data))
    print(successful_claim(data))


if __name__ == "__main__":
    main()
