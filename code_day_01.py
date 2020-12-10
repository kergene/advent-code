from itertools import combinations
from math import prod

def get_data():
    with open("input_day_1.txt") as f:
        data = f.read()
    data = data.splitlines()
    data = list(map(int, data))
    return data

def find_sum(data, n):
    for i in combinations(data, n):
        if sum(i) == 2020: return prod(i)

if __name__ == "__main__":
    data = get_data()
    print(find_sum(data, 2))
    print(find_sum(data, 3))

