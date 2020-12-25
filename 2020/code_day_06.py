def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    return data


def count_anyone(data):
    return sum(len(set(''.join(group.splitlines()))) for group in data)


def count_everyone(data):
    total = 0
    for group in data:
        everyone = set('acbdefghijklmnopqrstuvwxyz')
        for person in group.splitlines():
            everyone.intersection_update(set(person))
        total += len(everyone)
    return total    


def main():
    year, day = 2020, 6
    data = get_data(year, day)
    print(count_anyone(data))
    print(count_everyone(data))


if __name__ == "__main__":
    main()
