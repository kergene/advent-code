from collections import defaultdict
from collections import Counter


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(',')
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return int(datum)


def count_fish(data, days):
    fish_dict = Counter(data)
    for _ in range(days):
        new_dict = defaultdict(int)
        for fish, count in fish_dict.items():
            if fish == 0:
                new_dict[8] += count
                new_dict[6] += count
            else:
                new_dict[fish - 1] += count
        fish_dict = new_dict
    return sum(fish_dict.values())


def main():
    year, day = 2021, 6
    data = get_data(year, day)
    print(count_fish(data, 80))
    print(count_fish(data, 256))


if __name__ == "__main__":
    main()
