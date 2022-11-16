def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return [int(val) for val in datum]


def low_point_risk(data):
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    nrows = len(data)
    ncols = len(data[0])
    locations = {}
    for r in range(nrows):
        for c in range(ncols):
            locations[r, c] = data[r][c]
    tot_risk = 0
    for r in range(nrows):
        for c in range(ncols):
            flag = True
            for dr, dc in directions:
                if (r+dr, c+dc) in locations:
                    if locations[r, c] >= locations[r + dr, c + dc]:
                        flag = False
            if flag:
                tot_risk += 1 + locations[r, c]
    return tot_risk


def large_basins(data):
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    nrows = len(data)
    ncols = len(data[0])
    locations = {}
    for r in range(nrows):
        for c in range(ncols):
            locations[r, c] = data[r][c]
    low_points = set()
    for r in range(nrows):
        for c in range(ncols):
            flag = True
            for dr, dc in directions:
                if (r+dr, c+dc) in locations:
                    if locations[r, c] >= locations[r + dr, c + dc]:
                        flag = False
            if flag:
                low_points.add((r,c))
    basins = []
    for lowr, lowc in low_points:
        seen = set()
        basin = set()
        basin.add((lowr, lowc))
        while basin:
            r, c = basin.pop()
            seen.add((r, c))
            for dr, dc in directions:
                if (r+dr, c+dc) in locations and (r+dr, c+dc) not in seen:
                    if locations[r+dr, c+dc] != 9:
                        basin.add((r+dr, c+dc))
        basins.append(len(seen))
    basins = sorted(basins)
    return basins[-1] * basins[-2] * basins[-3]


def main():
    year, day = 2021, 9
    data = get_data(year, day)
    print(low_point_risk(data))
    print(large_basins(data))


if __name__ == "__main__":
    main()
