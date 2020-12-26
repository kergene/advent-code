from collections import Counter


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = datum.split('-')
    room = ' '.join(datum[:-1])
    end = datum[-1].split('[')
    num = int(end[0])
    check = end[1][:-1]
    return room, num, check


def validify(data):
    valid_rooms = []
    id_sum = 0
    for room, id_val, check in data:
        no_spaces = ''.join(room.split())
        count = Counter(no_spaces).most_common()
        count = sorted(count, key=lambda x:-26*x[1] + ord(x[0]))
        match = [count[i][0] for i in range(5)]
        if match == list(check):
            id_sum += id_val
            valid_rooms.append((room, id_val))
    return id_sum, valid_rooms


def find_north(data):
    for room, id_val in data:
        room = list(room)
        for i in range(len(room)):
            if room[i] == ' ':
                pass
            else:
                room[i] = chr((ord(room[i]) - 97 + id_val) % 26 + 97)
        room = ''.join(room)
        if 'north' in room:
            return id_val


def main():
    year, day = 2016, 4
    data = get_data(year, day)
    id_sum, valid_rooms = validify(data)
    print(id_sum)
    print(find_north(valid_rooms))


if __name__ == "__main__":
    main()
