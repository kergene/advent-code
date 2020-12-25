def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    sues_data = {'children': 3,
                 'cats': 7,
                 'samoyeds': 2,
                 'pomeranians': 3,
                 'akitas': 0,
                 'vizslas': 0,
                 'goldfish': 5,
                 'trees': 3,
                 'cars': 2,
                 'perfumes': 1
                }
    return data, sues_data


def preprocess(datum):
    datum = datum.split()[2:]
    for i in range(len(datum)):
        if datum[i][-1] in (',',':'):
            datum[i] = datum[i][:-1]
    categories = list(datum[i] for i in range(len(datum)) if i % 2 == 0)
    numbers = list(int(datum[i]) for i in range(len(datum)) if i % 2 == 1)
    return dict(i for i in zip(categories, numbers))


def which_sue(data, sues_data):
    for i in range(len(data)):
        sue = data[i]
        okay  = True
        for category, number in sue.items():
            if number != sues_data[category]:
                okay = False
                break
        if okay:
            return i + 1


def which_sue_ranged(data, sues_data):
    for i in range(len(data)):
        sue = data[i]
        okay  = True
        for category, number in sue.items():
            if category in ('cats', 'trees'):
                if number < sues_data[category]:
                    okay = False
                    break
            elif category in ('pomeranians', 'goldfish'):
                if number >= sues_data[category]:
                    okay = False
                    break
            elif number != sues_data[category]:
                okay = False
                break
        if okay:
            return i + 1


def main():
    year, day = 2015, 16
    data, sues_data = get_data(year, day)
    print(which_sue(data, sues_data))
    print(which_sue_ranged(data, sues_data))


if __name__ == "__main__":
    main()
