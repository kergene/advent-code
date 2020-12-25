from math import prod
from itertools import combinations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [int(datum) for datum in data]
    return data


def can_split(subset, target, n, min_group_size):
    for set_size in range(min_group_size, len(subset) // n + 1):
        for option in combinations(subset, set_size):
            if sum(option) == target:
                if n == 1:
                    return True
                else:
                    if can_split(subset.difference(option), target, n - 1, set_size):
                        return True
    return False


def balance_presents(weights, stacks):
    target = sum(weights) // stacks
    weights = set(weights)
    for min_group_size in range(1, len(weights) // stacks + 1):
        combis = combinations(weights, min_group_size)
        sorted_combis = sorted(combis, key=prod)
        for option in sorted_combis:
            if sum(option) == target:
                option = set(option)
                if can_split(weights.difference(option), target, stacks - 1, min_group_size):
                    return prod(option)


def main():
    year, day = 2015, 24
    weights = get_data(year, day)
    print(balance_presents(weights, 3))
    print(balance_presents(weights, 4))


if __name__ == "__main__":
    main()
