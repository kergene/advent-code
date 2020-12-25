from itertools import permutations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = dict(preprocess(datum) for datum in data)
    return data


def preprocess(datum):
    datum = datum.split()
    if datum[2] == 'gain':
        return ((datum[0], datum[-1][:-1]), int(datum[3]))
    else:
        return ((datum[0], datum[-1][:-1]), -int(datum[3]))


def find_max_happiness(data):
    people = set(pair[0] for pair in data)
    max_happiness = -abs(min(worth for worth in data.values()))*2*len(people)
    for ordering in permutations(people):
        new_happiness = get_happiness(ordering, data, True)
        if new_happiness > max_happiness:
            max_happiness = new_happiness
    return max_happiness


def get_happiness(ordering, data, wrap):
    happiness = 0
    for i in range(len(ordering) - 1):
        happiness += data[(ordering[i], ordering[i+1])]
        happiness += data[(ordering[i+1], ordering[i])]
    if wrap:
        happiness += data[(ordering[0], ordering[-1])]
        happiness += data[(ordering[-1], ordering[0])]
    return happiness


def find_max_happiness_no_wrap(data):
    people = set(pair[0] for pair in data)
    max_happiness = -abs(min(worth for worth in data.values()))*2*len(people)
    for ordering in permutations(people):
        new_happiness = get_happiness(ordering, data, False)
        if new_happiness > max_happiness:
            max_happiness = new_happiness
    return max_happiness


def main():
    year, day = 2015, 13
    data = get_data(year, day)
    print(find_max_happiness(data))
    print(find_max_happiness_no_wrap(data))


if __name__ == "__main__":
    main()
