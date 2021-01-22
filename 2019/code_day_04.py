from collections import Counter


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split('-')
    data = [preprocess(datum) for datum in data]
    return data

def preprocess(datum):
    return int(datum)


def is_increasing(n):
    if sorted(str(n)) == list(str(n)):
        return True


def has_repeat(n):
    n = str(n)
    for i in range(1, len(n)):
        if n[i] == n[i-1]:
            return True
    return False


def count_valids(data):
    count = 0
    for i in range(data[0], data[1] + 1):
        if is_increasing(i):
            if has_repeat(i):
                count += 1
    return count


def len_2_repeat(n):
    n = str(n)
    return 2 in Counter(n).values()


def count_valids_strong(data):
    count = 0
    for i in range(data[0], data[1] + 1):
        if is_increasing(i):
            if len_2_repeat(i):
                count += 1
    return count


def main():
    year, day = 2019, 4
    data = get_data(year, day)
    print(count_valids(data))
    print(count_valids_strong(data))


if __name__ == "__main__":
    main()
