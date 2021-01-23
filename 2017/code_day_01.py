def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    data = [int(datum) for datum in data]
    return data


def captcha_next(data):
    tot = 0
    for n in range(1, len(data)):
        if data[n] == data[n - 1]:
           tot += data[n]
    if data[0] == data[-1]:
        tot += data[0]
    return tot


def captcha_half(data):
    tot = 0
    length = len(data) // 2
    for n in range(length):
        if data[n] == data[n + length]:
            tot += 2 * data[n]
    return tot


def main():
    year, day = 2017, 1
    data = get_data(year, day)
    print(captcha_next(data))
    print(captcha_half(data))


if __name__ == "__main__":
    main()
