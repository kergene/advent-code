# a better approach to this question would be
# converting to travelling salesman problem

def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return list(datum)


def get_numbers(grid):
    NUMBERS = dict()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] in '0123456789':
                NUMBERS[grid[i][j]] = [i,j]
    return NUMBERS


def visit_all(grid):
    # each item in q is current node x, y followed by
    # 0 if corresponding number (1,...) has not been
    # visted, 1 if it has
    DIRECTIONS = ((-1,0), (1, 0), (0, -1), (0, 1))
    NUMBERS = get_numbers(grid)
    start = tuple(NUMBERS['0'] + [0] * (len(NUMBERS) - 1))
    NUMBERS.pop('0')
    q = set()
    q.add(start)
    DISTANCES = dict()
    DISTANCES[start] = 0
    while q:
        x, y, *nodes = choice = min(q, key=lambda x: DISTANCES[x])
        q.remove(choice)
        distance = DISTANCES[choice]
        if all(nodes):
            return distance
        for dx, dy in DIRECTIONS:
            a, b = x+dx, y+dy
            if 0 <= a < len(grid) and 0 <= b < len(grid[0]):
                if grid[a][b] != '#':
                    # can move here
                    nodes_copy = nodes.copy()
                    if grid[a][b] in NUMBERS:
                        nodes_copy[int(grid[a][b]) - 1] = 1
                    new_pos = tuple([a, b] + nodes_copy)
                    if new_pos in DISTANCES:
                        # only add to q if better than prev dist
                        if distance + 1 < DISTANCES[new_pos]:
                            q.add(new_pos)
                            DISTANCES[new_pos] = distance + 1
                    else:
                        # never got to here before
                        # add to q
                        q.add(new_pos)
                        DISTANCES[new_pos] = distance + 1


def visit_all_and_tidy(grid):
    # each item in q is current node x, y followed by
    # 0 if corresponding number (1,...) has not been
    # visted, 1 if it has
    DIRECTIONS = ((-1,0), (1, 0), (0, -1), (0, 1))
    NUMBERS = get_numbers(grid)
    origin = NUMBERS['0']
    start = tuple(NUMBERS['0'] + [0] * (len(NUMBERS) - 1))
    NUMBERS.pop('0')
    q = set()
    q.add(start)
    DISTANCES = dict()
    DISTANCES[start] = 0
    while q:
        x, y, *nodes = choice = min(q, key=lambda x: DISTANCES[x])
        q.remove(choice)
        distance = DISTANCES[choice]
        if all(nodes) and [x,y] == origin:
            return distance
        for dx, dy in DIRECTIONS:
            a, b = x+dx, y+dy
            if 0 <= a < len(grid) and 0 <= b < len(grid[0]):
                if grid[a][b] != '#':
                    # can move here
                    nodes_copy = nodes.copy()
                    if grid[a][b] in NUMBERS:
                        nodes_copy[int(grid[a][b]) - 1] = 1
                    new_pos = tuple([a, b] + nodes_copy)
                    if new_pos in DISTANCES:
                        # only add to q if better than prev dist
                        if distance + 1 < DISTANCES[new_pos]:
                            q.add(new_pos)
                            DISTANCES[new_pos] = distance + 1
                    else:
                        # never got to here before
                        # add to q
                        q.add(new_pos)
                        DISTANCES[new_pos] = distance + 1


def main():
    year, day = 2016, 24
    data = get_data(year, day)
    print(visit_all(data))
    print(visit_all_and_tidy(data))


if __name__ == "__main__":
    main()
