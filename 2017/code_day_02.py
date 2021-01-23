from itertools import combinations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = sorted(int(i) for i in datum.split())
    return datum


def max_min_diff(data):
    tot = 0
    for row in data:
        tot += max(row)
        tot -= min(row)
    return tot


def quotient_sum(data):
    tot = 0
    for row in data:
        for a, b in combinations(row, r=2):
            if b % a == 0:
                tot += b // a
                break
    return tot


def main():
    year, day = 2017, 2
    data = get_data(year, day)
    print(max_min_diff(data))
    print(quotient_sum(data))


if __name__ == "__main__":
    main()
