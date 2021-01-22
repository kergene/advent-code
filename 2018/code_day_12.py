from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    initial_state = list(data[0].split()[-1])
    data = dict(preprocess(datum) for datum in data[2:])
    return initial_state, data


def preprocess(datum):
    datum = datum.replace('#', '1').replace('.', '0').split(' => ')
    return datum[0], datum[1]


def spread(pots, rules):
    new_pots = defaultdict(int)
    min_idx = min(pots)
    max_idx = max(pots)
    for idx in range(min_idx - 2, max_idx + 3):
        new_pots[idx] = rules[''.join(str(pots[i]) for i in range(idx - 2, idx + 3))]
    return new_pots


def pots_potted(initial_state, rules):
    pots = defaultdict(int)
    for idx, value in enumerate(initial_state):
        pots[idx] = int(value == '#')
    for _ in range(20):
        pots = spread(pots, rules)
    return score_plants(pots)


def score_plants(pots):
    return sum(k for k, v in pots.items() if v == '1')


def long_pots_potted(initial_state, rules):
    pots = defaultdict(int)
    for idx, value in enumerate(initial_state):
        pots[idx] = int(value == '#')
    score = score_plants(pots)
    diffs = [None]
    i = 0
    while True:
        i += 1
        pots = spread(pots, rules)
        score, last = score_plants(pots), score
        diff = score - last
        if diff == diffs[-1] == diffs[-2]:
            return (50000000000 - i) * diff + score
        else:
            diffs.append(diff)


def main():
    year, day = 2018, 12
    initial_state, data = get_data(year, day)
    print(pots_potted(initial_state, data))
    print(long_pots_potted(initial_state, data))


if __name__ == "__main__":
    main()
