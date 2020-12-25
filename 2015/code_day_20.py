from math import ceil


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return int(data)


def elves(data): # not space efficient, but faster
    sum_elves = data // 10
    totals = [0 for i in range(sum_elves)]
    for elf in range(1, sum_elves + 1):
        for j in range(elf, sum_elves, elf):
            totals[j - 1] += elf
        if totals[elf - 1] >= sum_elves:
            return elf


def lazy_elves(data):
    # house can't be lower than min_test
    sum_elves = ceil(data // 11)
    min_test = int(sum_elves // sum(1/i for i in range(1, 51)))
    n = min_test
    while True:
        tot = 0
        for i in range(1, 51):
            if n % i == 0:
                tot += n // i
        if tot >= sum_elves:
            return n
        else:
            n += 1


def main():
    year, day = 2015, 20
    data = get_data(year, day)
    print(elves(data))
    print(lazy_elves(data))


if __name__ == "__main__":
    main()
