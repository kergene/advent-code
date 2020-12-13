from math import prod

def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data[0] = int(data[0])
    data[1] = preprocess(data[1])
    return data

def preprocess(timetable):
    timetable = timetable.split(',')
    timetable = [int(i) if i != 'x' else -1 for i in timetable]
    return timetable

def bezout(a, b):
    remainder = min(a, b)
    gcd = max(a, b)
    quotients = []
    while remainder:
        quotients.append(gcd // remainder)
        gcd, remainder = remainder, gcd % remainder
    quotients.pop()
    if not quotients:
        if a > b:
            return b, 0, 1
        else:
            return a, 1, 0
    else:
        coef_1 = 1
        coef_2 = -quotients.pop()
        while quotients:
            coef_1, coef_2 = coef_2, coef_1 - coef_2 * quotients.pop(),
        if a > b:
            return gcd, coef_1, coef_2
        else:
            return gcd, coef_2, coef_1

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
    buses = [(buses[i], (buses[i]  - i) % buses[i]) for i in range(len(buses)) if buses[i] != -1]
    remainder = buses[0][1]
    mod = buses[0][0]
    for new_mod, new_remainder in buses[1:]:
        coefs = bezout(mod, new_mod)
        remainder = remainder * new_mod * coefs[2] + new_remainder * mod * coefs[1]
        mod = mod * new_mod // coefs[0]
        remainder = remainder % mod
    return remainder

def main():
    day = 13
    data = get_data(day)
    print(next_bus(data))
    print(bus_schedule(data))

if __name__ == "__main__":
    main()
