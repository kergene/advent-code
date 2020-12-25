from math import prod
from itertools import product


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = list(preprocess(datum) for datum in data)
    return data


def preprocess(datum):
    datum = datum.split()
    return [int(datum[2][:-1]),
            int(datum[4][:-1]),
            int(datum[6][:-1]),
            int(datum[8][:-1]),
            int(datum[10])
    ]


def unrestricted_score(data):
    max_score = 0
    for amounts in product(range(101), repeat=3):
        if sum(amounts) > 100:
            continue
        else:
            amounts = list(amounts)
            amounts.append(100 - sum(amounts))
            score = 1
            for category in range(4):
                cat_values = [row[category] for row in data]
                score *= max(sum(prod(i) for i in zip(cat_values, amounts)),0)
            if score > max_score:
                max_score = score
    return max_score


def fixed_calories_score(data):
    max_score = 0
    for amounts in product(range(101), repeat=3):
        if sum(amounts) > 100:
            continue
        else:
            amounts = list(amounts)
            amounts.append(100 - sum(amounts))
            cals = [row[4] for row in data]
            if sum(prod(i) for i in zip(cals, amounts)) != 500:
                continue
            else:
                score = 1
                for category in range(4):
                    cat_values = [row[category] for row in data]
                    score *= max(sum(prod(i) for i in zip(cat_values, amounts)),0)
                if score > max_score:
                    max_score = score
    return max_score


def main():
    year, day = 2015, 15
    data = get_data(year, day)
    print(unrestricted_score(data))
    print(fixed_calories_score(data))


if __name__ == "__main__":
    main()
