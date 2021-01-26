def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = set(preprocess(datum) for datum in data)
    return data


def preprocess(datum):
    return tuple(int(val) for val in datum.split(','))


def constellations(data):
    count = 0
    while data:
        count += 1
        # pick element without removing it
        star = data.pop()
        data.add(star)
        q = set()
        q.add(star)
        while q:
            choice = q.pop()
            data.remove(choice)
            for cell in data:
                if mannhattan_distance(choice, cell) <= 3:
                    q.add(cell)
    return count


def mannhattan_distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def main():
    year, day = 2018, 25
    data = get_data(year, day)
    print(constellations(data))


if __name__ == "__main__":
    main()
