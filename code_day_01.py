from itertools import combinations
from math import prod


def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = list(int(i) for i in data)
    return data


def find_n_sum(data, n, target=2020):
    if n > 2:
        for idx in range(len(data) - 1):
            value = data[idx]
            product, found = find_n_sum(data[idx+1:], n - 1, target - value)
            if found:
                return value * product, True
        else:
            return 0, False
    else:
        minus = set()
        for value in data:
            if value in minus:
                return value * (target - value), True
            else:
                minus.add(target - value)
        else:
            return 0, False


def main():
    day = 1
    data = get_data(day)
    print(find_n_sum(data, 2)[0])
    print(find_n_sum(data, 3)[0])


if __name__ == "__main__":
    main()
