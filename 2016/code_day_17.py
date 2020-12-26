import hashlib


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return data


def get_room(choice):
    row = choice.count('D') - choice.count('U')
    col = choice.count('R') - choice.count('L')
    return row, col


def shortest_path(passcode):
    paths = set(('',))
    target = (3,3)
    allowed = 'bcdef'
    while paths:
        choice = min(paths, key=len)
        paths.remove(choice)
        room = get_room(choice)
        if room == target:
            return choice
        to_hash = passcode + choice
        hashed = hashlib.md5(to_hash.encode('utf-8')).hexdigest()[:4]
        if room[0] != 0 and hashed[0] in allowed:
            # can move up
            paths.add(choice + 'U')
        if room[0] != 3 and hashed[1] in allowed:
            # can move down
            paths.add(choice + 'D')
        if room[1] != 0 and hashed[2] in allowed:
            # can move left
            paths.add(choice + 'L')
        if room[1] != 3 and hashed[3] in allowed:
            # can move right
            paths.add(choice + 'R')


def longest_path(passcode):
    paths = set(('',))
    target = (3,3)
    allowed = 'bcdef'
    longest = 0
    while paths:
        choice = min(paths, key=len)
        paths.remove(choice)
        room = get_room(choice)
        if room == target:
            longest = len(choice)
        else:
            to_hash = passcode + choice
            hashed = hashlib.md5(to_hash.encode('utf-8')).hexdigest()[:4]
            if room[0] != 0 and hashed[0] in allowed:
                # can move up
                paths.add(choice + 'U')
            if room[0] != 3 and hashed[1] in allowed:
                # can move down
                paths.add(choice + 'D')
            if room[1] != 0 and hashed[2] in allowed:
                # can move left
                paths.add(choice + 'L')
            if room[1] != 3 and hashed[3] in allowed:
                # can move right
                paths.add(choice + 'R')
    return longest


def main():
    year, day = 2016, 17
    data = get_data(year, day)
    print(shortest_path(data))
    print(longest_path(data))


if __name__ == "__main__":
    main()
