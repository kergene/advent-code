def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [int(datum) for datum in data]
    return data


def open_door(card_pub, door_pub):
    MODULO = 20201227
    value = 1
    subject = 7
    card_loop_size = 0
    while value != card_pub:
        value = (value * subject) % MODULO
        card_loop_size += 1
    subject = door_pub
    value = 1
    for _ in range(card_loop_size):
        value = (value * subject) % MODULO
    return value


def main():
    day = 25
    card_pub, door_pub = get_data(day)
    print(open_door(card_pub, door_pub))


if __name__ == "__main__":
    main()
