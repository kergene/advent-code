def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return [int(i) for i in datum.split()]


def triangles(data):
    total = 0
    for line in data:
        line = sorted(line)
        if line[0] + line[1] > line[2]:
            total += 1
    return total


def vertical_triangles(data):
    total = 0
    line_num = 0
    while line_num < len(data):
        lines = zip(*data[line_num:line_num + 3])
        lines = [sorted(i) for i in lines]
        for line in lines:
            if line[0] + line[1] > line[2]:
                total += 1
        line_num += 3
    return total


def main():
    year, day = 2016, 3
    data = get_data(year, day)
    print(triangles(data))
    print(vertical_triangles(data))


if __name__ == "__main__":
    main()
