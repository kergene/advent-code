def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(',')
    data = [int(datum) for datum in data]
    return data


def find_nth_term(data, n):
    index_lookup = {}
    for idx, val in enumerate(data[:-1]):
        index_lookup[val] = idx
    last = data[-1]
    for i in range(len(data), n):
        if last in index_lookup:
            next_term = i - index_lookup[last] - 1
            index_lookup[last] = i - 1
            last = next_term
        else:
            next_term = 0
            index_lookup[last] = i - 1
            last = next_term
    return last


def main():
    year, day = 2020, 15
    data = get_data(year, day)
    print(find_nth_term(data, 2020))
    print(find_nth_term(data, 30000000))


if __name__ == "__main__":
    main()
