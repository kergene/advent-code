def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return 1 if datum == '^' else 0


def get_next_row(data):
    data = [0] + data + [0]
    new_data = []
    for i in range(1, len(data) - 1):
        if data[i - 1] == 1 and data[i] == 1 and data[i+1] == 0:
            new_data.append(1)
        elif data[i - 1] == 0 and data[i] == 1 and data[i+1] == 1:
            new_data.append(1)
        elif data[i - 1] == 1 and data[i] == 0 and data[i+1] == 0:
            new_data.append(1)
        elif data[i - 1] == 0 and data[i] == 0 and data[i+1] == 1:
            new_data.append(1)
        else:
            new_data.append(0)
    return new_data


def count_mines(data, rows):
    mines = sum(data)
    total_squares = len(data) * rows
    for _ in range(rows - 1):
        data = get_next_row(data)
        mines += sum(data)
    return total_squares - mines


def main():
    year, day = 2016, 18
    data = get_data(year, day)
    print(count_mines(data, 40))
    print(count_mines(data, 400000))


if __name__ == "__main__":
    main()
