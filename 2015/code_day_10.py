def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return data


def look_and_say(data):
    new = []
    current = data[0]
    j = 1
    for i in range(1, len(data)):
        if data[i] == current:
            j += 1
        else:
            new.append(j)
            new.append(current)
            j = 1
            current = data[i]
    new.append(j)
    new.append(current)
    return new


def repeater(data):
    data = list(int(i) for i in data)
    for _ in range(40):
        data = look_and_say(data)
    part_1_ans = len(data)
    for _ in range(10):
        data = look_and_say(data)
    return part_1_ans, len(data)


def main():
    year, day = 2015, 10
    data = get_data(year, day)
    r40, r50 = repeater(data)
    print(r40)
    print(r50)


if __name__ == "__main__":
    main()
