from heapdict import heapdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return [int(val) for val in datum]


def find_path(data, multiplier):
    DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
    data_dict = {}
    nrows = len(data)
    ncols = len(data[0])
    for rmult in range(multiplier):
        for cmult in range(multiplier):
            for r in range(nrows):
                for c in range(ncols):
                    risk = (data[r][c] + rmult + cmult) % 9
                    data_dict[r + nrows*rmult, c + ncols*cmult] = risk if risk != 0 else 9
    target = (multiplier*nrows - 1, multiplier*ncols - 1)
    start = (0, 0)
    risks = heapdict()
    seens = set()
    risks[start] = 0
    while risks:
        pos, risk = risks.popitem()
        seens.add(pos)
        if pos == target:
            return risk
        r, c = pos
        for dr, dc in DIRECTIONS:
            new_pos = r + dr, c + dc
            if new_pos not in seens and new_pos in data_dict:
                new_risk = data_dict[new_pos] + risk
                if new_pos in risks:
                    if risks[new_pos] > new_risk:
                        risks[new_pos] = new_risk
                else:
                    risks[new_pos] = new_risk


def main():
    year, day = 2021, 15
    data = get_data(year, day)
    print(find_path(data, 1))
    print(find_path(data, 5))


if __name__ == "__main__":
    main()
