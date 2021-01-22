def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [int(datum) for datum in data]
    return data


def resulting_frequency(data):
    return sum(line for line in data)


def repeated_frequency(data):
    seens = set()
    freq = 0
    seens.add(freq)
    while True:
        for line in data:
            freq += line
            if freq in seens:
                return freq
            else:
                seens.add(freq)


def main():
    year, day = 2018, 1
    data = get_data(year, day)
    print(resulting_frequency(data))
    print(repeated_frequency(data))


if __name__ == "__main__":
    main()
