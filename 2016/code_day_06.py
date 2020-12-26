from collections import Counter


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [list(datum) for datum in data]
    return data


def most_common(data):
    message = []
    data = zip(*data)
    for i in data:
        message.append(Counter(i).most_common(1)[0][0])
    return ''.join(message)


def least_common(data):
    message = []
    data = zip(*data)
    for i in data:
        message.append(Counter(i).most_common()[-1][0])
    return ''.join(message)


def main():
    year, day = 2016, 6
    data = get_data(year, day)
    print(most_common(data))
    print(least_common(data))


if __name__ == "__main__":
    main()
