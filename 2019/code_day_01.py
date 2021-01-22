def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return int(datum)


def module_fuels(data):
    return sum(n // 3 - 2 for n in data)


def total_fuels(data):
    total_fuel = 0
    for n in data:
        module_fuel = 0
        n = n // 3 - 2
        while n > 0:
            module_fuel += n
            n = n // 3 - 2
        total_fuel += module_fuel
    return total_fuel


def main():
    year, day = 2019, 1
    data = get_data(year, day)
    print(module_fuels(data))
    print(total_fuels(data))


if __name__ == "__main__":
    main()
