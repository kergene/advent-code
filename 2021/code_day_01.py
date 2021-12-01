def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return int(datum)


def increasing_count(data):
    count = 0
    for idx in range(1, len(data)):
        if data[idx] > data[idx - 1]:
            count += 1
    return count


def increasing_sum(data):
    count = 0
    for idx in range(3, len(data)):
        if data[idx] > data[idx - 3]:
            count += 1
    return count


def main():
    year, day = 2021, 1
    data = get_data(year, day)
    print(increasing_count(data))
    print(increasing_sum(data))


if __name__ == "__main__":
    main()
