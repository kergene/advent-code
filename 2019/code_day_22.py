def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum


def shuffle_cards(data):
    n_cards = 10007
    cards = list(range(n_cards))
    for line in data:
        line = line.split()
        if line[0] == 'deal':
            if line[1] == 'into':
                cards = cards[::-1]
            else:
                increment = int(line[-1])
                inv = pow(increment, -1, n_cards)
                cards = [cards[(idx * inv) % n_cards] for idx in range(n_cards)]
        else:
            cut = int(line[1])
            cards = cards[cut:] + cards[:cut]
    return cards.index(2019)


def run_loop(target, data, n_cards):
    for line in data:
        line = line.split()
        if line[0] == 'deal':
            if line[1] == 'into':
                target = n_cards - 1 - target
            else:
                increment = int(line[-1])
                target *= increment
                target %= n_cards
        else:
            cut = int(line[1])
            target -= cut
            target %= n_cards
    return target


def super_shuffle_cards(data):
    n_cards = 119315717514047
    repeats = 101741582076661
    add = run_loop(0, data, n_cards)
    times = run_loop(1, data, n_cards) - add
    target = 2020
    const = (add * (pow(times, repeats, n_cards) - 1) * (pow(times - 1, -1, n_cards))) % n_cards
    return ((target - const) * pow(times, -repeats, n_cards)) % n_cards


def main():
    year, day = 2019, 22
    data = get_data(year, day)
    print(shuffle_cards(data))
    print(super_shuffle_cards(data))


if __name__ == "__main__":
    main()
