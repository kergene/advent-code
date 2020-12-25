def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def length_diff(rules):
    return sum(len(i) - len(eval(i)) for i in rules)


def new_encoding(rules):
    diff = 2*len(rules)
    rules = ''.join(rules)
    diff += rules.count('"')
    diff += rules.count('\\')
    return diff


def main():
    year, day = 2015, 8
    rules = get_data(year, day)
    print(length_diff(rules))
    print(new_encoding(rules))


if __name__ == "__main__":
    main()
