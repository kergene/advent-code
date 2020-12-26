def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum.split()


def scramble(data):
    password = list('abcdefgh')
    for line in data:
        if line[0] == 'swap':
            if line[1] == 'position':
                idx_1 = int(line[2])
                idx_2 = int(line[-1])
                password[idx_1], password[idx_2] = password[idx_2], password[idx_1]
            elif line[1] == 'letter':
                idx_1 = password.index(line[2])
                idx_2 = password.index(line[-1])
                password[idx_1], password[idx_2] = line[-1], line[2]
            else:
                assert False
        elif line[0] == 'reverse':
            idx_1 = int(line[2])
            idx_2 = int(line[-1])
            password[idx_1:idx_2 + 1] = reversed(password[idx_1:idx_2 + 1])
        elif line[0] == 'move':
            idx_1 = int(line[2])
            idx_2 = int(line[-1])
            removed = password.pop(idx_1)
            password = password[:idx_2] + [removed] + password[idx_2:]
        elif line[0] == 'rotate':
            if line[1] == 'based':
                idx_1 = password.index(line[-1])
                password = password[-idx_1:] + password[:-idx_1]
                password = password[-1:] + password[:-1]
                if idx_1 >= 4:
                    password = password[-1:] + password[:-1]
            elif line[1] == 'left':
                idx_1 = int(line[2])
                password = password[idx_1:] + password[:idx_1]
            elif line[1] == 'right':
                idx_1 = int(line[2])
                password = password[-idx_1:] + password[:-idx_1]
            else:
                assert False
        else:
            assert False
    return ''.join(password)


def unscramble(data):
    password = list('fbgdceah')
    for line in reversed(data):
        if line[0] == 'swap':
            if line[1] == 'position':
                # no change
                idx_1 = int(line[2])
                idx_2 = int(line[-1])
                password[idx_1], password[idx_2] = password[idx_2], password[idx_1]
            elif line[1] == 'letter':
                # no change
                idx_1 = password.index(line[2])
                idx_2 = password.index(line[-1])
                password[idx_1], password[idx_2] = line[-1], line[2]
            else:
                assert False
        elif line[0] == 'reverse':
            # no change
            idx_1 = int(line[2])
            idx_2 = int(line[-1])
            password[idx_1:idx_2 + 1] = reversed(password[idx_1:idx_2 + 1])
        elif line[0] == 'move':
            # indices 1 and 2 are swapped
            idx_1 = int(line[2])
            idx_2 = int(line[-1])
            removed = password.pop(idx_2)
            password = password[:idx_1] + [removed] + password[idx_1:]
        elif line[0] == 'rotate':
            if line[1] == 'based':
                # go other way
                idx_out = password.index(line[-1])
                selection = '70415263'
                idx_1 = int(selection[idx_out])
                password = password[idx_1:] + password[:idx_1]
                password = password[1:] + password[:1]
                if idx_1 >= 4:
                    password = password[1:] + password[:1]
            elif line[1] == 'right':
                # go other way
                idx_1 = int(line[2])
                password = password[idx_1:] + password[:idx_1]
            elif line[1] == 'left':
                # go other way
                idx_1 = int(line[2])
                password = password[-idx_1:] + password[:-idx_1]
            else:
                assert False
        else:
            assert False
    return ''.join(password)


def main():
    year, day = 2016, 21
    data = get_data(year, day)
    print(scramble(data))
    print(unscramble(data))


if __name__ == "__main__":
    main()
