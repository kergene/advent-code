def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return data


def count_houses(directions):
    location = [0,0]
    seens = set((tuple(location),))
    for step in directions:
        if step == '^':
            location[1] += 1
        elif step == '>':
            location[0] += 1
        elif step == '<':
            location[0] -= 1
        else:
            location[1] -= 1
        seens.add(tuple(location))
    return len(seens)


def count_houses_robo(directions):
    location = [[0,0],[0,0]]
    mover = 0
    seens = set(((0,0),))
    for step in directions:
        if step == '^':
            location[mover][1] += 1
        elif step == '>':
            location[mover][0] += 1
        elif step == '<':
            location[mover][0] -= 1
        else:
            location[mover][1] -= 1
        seens.add(tuple(location[mover]))
        mover = 1 - mover
    return len(seens)


def main():
    year, day = 2015, 3
    directions = get_data(year, day)
    print(count_houses(directions))
    print(count_houses_robo(directions))


if __name__ == "__main__":
   main()
