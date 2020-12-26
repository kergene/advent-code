def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return int(data)


def check_cell(x, y, n):
    val = x*x + 3*x + 2*x*y + y + y*y + n
    val = bin(val)[2:]
    return 1 - sum(int(i) for i in val) % 2


def shortest_path(n):
    DIRECTIONS = ((-1, 0), (1,0), (0, -1), (0, 1))
    q = set(((1,1),))
    DISTANCES = {}
    DISTANCES[(1,1)] = 0
    target = (31,39)
    while q:
        choice = min(q, key=lambda x: DISTANCES[x])
        q.remove(choice)
        distance = DISTANCES[choice]
        if choice == target:
            return distance
        else:
            x, y = choice
            for dx, dy in DIRECTIONS:
                if x+dx >= 0 and y+dy>=0:
                    a, b = x+dx, y+dy
                    if check_cell(a, b, n):
                        if (a,b) in DISTANCES:
                            if distance + 1 < DISTANCES[(a,b)]:
                                q.add((a, b))
                                DISTANCES[(a,b)] = distance + 1
                        else:
                            q.add((a, b))
                            DISTANCES[(a,b)] = distance + 1


def reachable_cells(n):
    DIRECTIONS = ((-1, 0), (1,0), (0, -1), (0, 1))
    q = set(((1,1),))
    seens = set()
    DISTANCES = {}
    DISTANCES[(1,1)] = 0
    while q:
        choice = min(q, key=lambda x: DISTANCES[x])
        q.remove(choice)
        seens.add(choice)
        distance = DISTANCES[choice]
        if distance < 50:
            x, y = choice
            for dx, dy in DIRECTIONS:
                if x+dx >= 0 and y+dy>=0:
                    a, b = x+dx, y+dy
                    if check_cell(a, b, n):
                        if (a,b) in DISTANCES:
                            if distance + 1 < DISTANCES[(a,b)]:
                                q.add((a, b))
                                DISTANCES[(a,b)] = distance + 1
                        else:
                            q.add((a, b))
                            DISTANCES[(a,b)] = distance + 1
    return len(seens)


def main():
    year, day = 2016, 13
    data = get_data(year, day)
    print(shortest_path(data))
    print(reachable_cells(data))


if __name__ == "__main__":
    main()
