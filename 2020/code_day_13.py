from math import prod


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data[0] = int(data[0])
    data[1] = preprocess(data[1])
    return data


def preprocess(timetable):
    timetable = timetable.split(',')
    timetable = [int(i) if i != 'x' else -1 for i in timetable]
    return timetable


def next_bus(data):
    time = data[0]
    buses = data[1]
    min_wait = max(buses)
    for bus_mod in buses:
        if bus_mod != -1:
            wait = bus_mod - (time % bus_mod)
            if wait < min_wait:
                min_bus = bus_mod
                min_wait = wait
    return min_wait * min_bus


def bus_schedule(data):
    buses = data[1]
    buses = [(buses[i], (- i) % buses[i]) for i in range(len(buses)) if buses[i] != -1]
    N = prod(bus[0] for bus in buses)
    total = 0
    for mod, rem in buses:
        b = N // mod
        total += b * rem * pow(b, -1, mod)
    return total % N


def main():
    year, day = 2020, 13
    data = get_data(year, day)
    print(next_bus(data))
    print(bus_schedule(data))


if __name__ == "__main__":
    main()
