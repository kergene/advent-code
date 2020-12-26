from itertools import product


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return preprocess(data)


def preprocess(data):
    REPLACE = {'F':'0',
               'B':'1',
               'L':'0',
               'R':'1'}
    for old, new in REPLACE.items():
        data = data.replace(old, new)
    return set(int(string, 2) for string in data.splitlines())


def check_cards(data):
    return max(data)


def find_card(data, max_seat):
    seat_id = max_seat
    while True:
        if seat_id not in data:
            return seat_id
        seat_id -= 1


def main():
    year, day = 2020, 5
    data = get_data(year, day)
    max_seat = check_cards(data)
    print(max_seat)
    print(find_card(data, max_seat))


if __name__ == "__main__":
    main()
