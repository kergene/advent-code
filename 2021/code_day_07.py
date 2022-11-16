def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(',')
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return int(datum)


def align_crabs(data):
    data = sorted(data)
    median = data[len(data) // 2]
    return sum(abs(median - x) for x in data)


def cost(n):
    return n * (n + 1) // 2


def expensive_align_crabs(data):
    best_fuel = len(data)*max(data)**2
    for h in range(max(data)):
        fuel = sum(cost(abs(pos - h)) for pos in data)
        if fuel < best_fuel:
            best_fuel = fuel
    return best_fuel


def main():
    year, day = 2021, 7
    data = get_data(year, day)
    print(align_crabs(data))
    print(expensive_align_crabs(data))


if __name__ == "__main__":
    main()
