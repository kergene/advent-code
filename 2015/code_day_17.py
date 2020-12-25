from math import prod
from itertools import product


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [int(datum) for datum in data]
    return data


def count_sums(data):
    target = 150
    counter = 0
    for binary in product((0,1), repeat=len(data)):
        if sum(prod(j) for j in zip(binary, data)) == target:
            counter += 1
    return counter


def count_min_sums(data):
    target = 150
    min_containers = len(data)
    for i in product((0,1), repeat=len(data)):
        if sum(prod(j) for j in zip(i, data)) == target:
            min_containers = min(min_containers, sum(i))
    counter = 0
    for binary in product((0,1), repeat=len(data)):
        if sum(binary) == min_containers:
            if sum(prod(j) for j in zip(binary, data)) == target:
                counter += 1
    return counter


def main():
    year, day = 2015, 17
    data = get_data(year, day)
    print(count_sums(data))
    print(count_min_sums(data))


if __name__ == "__main__":
    main()
