from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    polymer, rules = data
    rules = dict(preprocess(datum) for datum in rules.splitlines())
    return polymer, rules


def preprocess(datum):
    return tuple(datum.split(' -> '))


def synthesise(polymer, rules, repeats):
    segments = defaultdict(int)
    for idx in range(len(polymer) - 1):
        segments[polymer[idx:idx + 2]] += 1
    for _ in range(repeats):
        new_segments = defaultdict(int)
        for pair, count in segments.items():
            new_letter = rules[pair]
            new_segments[''.join([pair[0], new_letter])] += count
            new_segments[''.join([new_letter, pair[1]])] += count
        segments = new_segments
    counter = defaultdict(int)
    for pair, count in segments.items():
        counter[pair[0]] += count
        counter[pair[1]] += count
    counter[polymer[0]] += 1
    counter[polymer[-1]] += 1
    vals = sorted(counter.values())
    return (vals[-1] - vals[0]) // 2


def main():
    year, day = 2021, 14
    polymer, rules = get_data(year, day)
    print(synthesise(polymer, rules, 10))
    print(synthesise(polymer, rules, 40))


if __name__ == "__main__":
    main()
