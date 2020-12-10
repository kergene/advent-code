from itertools import combinations
from math import prod

def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = list(int(i) for i in data)
    return data

def find_sum(data, n):
    for i in combinations(data, n):
        if sum(i) == 2020: return prod(i)

def main():
    day = 1
    data = get_data(day)
    print(find_sum(data, 2))
    print(find_sum(data, 3))

if __name__ == "__main__":
    main()
