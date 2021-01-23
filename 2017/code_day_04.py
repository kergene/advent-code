from collections import Counter


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum.split()


def unique_wordlists(data):
    return sum(Counter(row).most_common(1)[0][1] == 1 for row in data)


def no_anagrams(data):
    data = [[''.join(sorted(word)) for word in datum] for datum in data]
    return unique_wordlists(data)


def main():
    year, day = 2017, 4
    data = get_data(year, day)
    print(unique_wordlists(data))
    print(no_anagrams(data))


if __name__ == "__main__":
    main()
