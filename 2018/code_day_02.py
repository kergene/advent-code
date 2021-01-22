from collections import Counter


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum


def id_checksum(data):
    threes = twos = 0
    for word in data:
        c = Counter(word)
        threes += any(count == 3 for count in c.values())
        twos += any(count == 2 for count in c.values())
    return threes * twos


def similar_ids(data):
    seens = set()
    for word in data:
        for idx in range(len(word)):
            test = word[:idx] + '0' + word[idx + 1:]
            if test in seens:
                return test.replace('0', '')
            else:
                seens.add(test)


def main():
    year, day = 2018, 2
    data = get_data(year, day)
    print(id_checksum(data))
    print(similar_ids(data))


if __name__ == "__main__":
    main()
