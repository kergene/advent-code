def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def move_cucumbers(data):
    max_idx = len(data), len(data[0])
    downs = set()
    rights = set()
    for r_idx, row in enumerate(data):
        for c_idx, value in enumerate(row):
            if value == 'v':
                downs.add((r_idx, c_idx))
            elif value == '>':
                rights.add((r_idx, c_idx))
    flag = False
    count = 0
    while not flag:
        flag, rights, downs = take_step(rights, downs, max_idx)
        count += 1
    return count


def take_step(rights, downs, max_idx):
    flag = True
    new_rights = set()
    for cucumber in rights:
        r_idx, c_idx = cucumber
        if c_idx + 1 == max_idx[1]:
            new_cucumber = (r_idx, 0)
        else:
            new_cucumber = (r_idx, c_idx + 1)
        if new_cucumber not in rights and new_cucumber not in downs:
            new_rights.add(new_cucumber)
            flag = False
        else:
            new_rights.add(cucumber)
    new_downs = set()
    for cucumber in downs:
        r_idx, c_idx = cucumber
        if r_idx + 1 == max_idx[0]:
            new_cucumber = (0, c_idx)
        else:
            new_cucumber = (r_idx + 1, c_idx)
        if new_cucumber not in new_rights and new_cucumber not in downs:
            new_downs.add(new_cucumber)
            flag = False
        else:
            new_downs.add(cucumber)
    return flag, new_rights, new_downs


def main():
    year, day = 2021, 25
    data = get_data(year, day)
    print(move_cucumbers(data))


if __name__ == "__main__":
    main()
