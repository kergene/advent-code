from heapdict import heapdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum


'''
Note: we could speed things up slightly by caching
distances between the jumps (would save any
intermediate steps)
Part 2 reaches depth of 121 in loops!
'''


def solve_maze(grid):
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
    n_rows = len(grid)
    n_cols = len(grid[0])
    pairings = dict()
    jumps = dict()
    count = 0
    # create list of jumps that we can move with
    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c] in ALPHABET:
                for dr, dc in DIRECTIONS:
                    r2, c2 = r + dr, c + dc
                    r3, c3 = r2 + dr, c2 + dc
                    if 0 <= r3 < n_rows and 0 <= c3 < n_cols:
                        if grid[r2][c2] in ALPHABET:
                            if grid[r3][c3] == '.':
                                pair = ''.join(sorted([grid[r2][c2], grid[r][c]]))
                                count += 1
                                if pair in pairings:
                                    jumps[r3, c3] = pairings[pair]
                                    jumps[pairings[pair]] = r3, c3
                                else:
                                    pairings[pair] = r3, c3
    # dijkstra's style algo
    start = pairings['AA']
    finish = pairings['ZZ']
    distances = heapdict()
    distances[start] = 0
    seens = set()
    while distances:
        choice, distance = distances.popitem()
        seens.add(choice)
        if choice == finish:
            return distance
        r, c = choice
        for dr, dc in DIRECTIONS:
            a, b = pos = r + dr, c + dc
            if grid[a][b] == '.':
                if pos not in seens:
                    if pos in distances:
                        if distances[pos] > distance + 1:
                            distances[pos] = distance + 1
                    else:
                        distances[pos] = distance + 1
        # 'jumping' edges
        if choice in jumps:
            pos = jumps[choice]
            if pos not in seens:
                if pos in distances:
                    if distances[pos] > distance + 1:
                        distances[pos] = distance + 1
                else:
                    distances[pos] = distance + 1
    assert False


def solve_maze_recursive(grid):
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
    n_rows = len(grid)
    n_cols = len(grid[0])
    pairings = dict()
    outers = dict()
    inners = dict()
    count = 0
    # create list of jumps that we can move with
    # separately for outer/inner
    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c] in ALPHABET:
                for dr, dc in DIRECTIONS:
                    r2, c2 = r + dr, c + dc
                    r3, c3 = r2 + dr, c2 + dc
                    if 0 <= r3 < n_rows and 0 <= c3 < n_cols:
                        if grid[r2][c2] in ALPHABET:
                            if grid[r3][c3] == '.':
                                pair = ''.join(sorted([grid[r2][c2], grid[r][c]]))
                                count += 1
                                if pair in pairings:
                                    if r in (0, n_rows - 1) or c in (0, n_cols - 1):
                                        outers[r3, c3] = pairings[pair]
                                        inners[pairings[pair]] = r3, c3
                                    else:
                                        inners[r3, c3] = pairings[pair]
                                        outers[pairings[pair]] = r3, c3
                                else:
                                    pairings[pair] = r3, c3
    # dijkstra's style algo
    start = tuple(list(pairings['AA']) + [0])
    finish = tuple(list(pairings['ZZ']) + [0])
    distances = heapdict()
    distances[start] = 0
    seens = set()
    while distances:
        choice, distance = distances.popitem()
        seens.add(choice)
        if choice == finish:
            return distance
        r, c, level = choice
        for dr, dc in DIRECTIONS:
            a, b, _ = pos = r + dr, c + dc, level
            if grid[a][b] == '.':
                if pos not in seens:
                    if pos in distances:
                        if distances[pos] > distance + 1:
                            distances[pos] = distance + 1
                    else:
                        distances[pos] = distance + 1
        # 'jumping' out edges
        if (r, c) in outers and level > 0:
            pos = tuple(list(outers[r, c]) + [level - 1])
            if pos not in seens:
                if pos in distances:
                    if distances[pos] > distance + 1:
                        distances[pos] = distance + 1
                else:
                    distances[pos] = distance + 1
        # 'jumping' in edges
        if (r, c) in inners:
            pos = tuple(list(inners[r, c]) + [level + 1])
            if pos not in seens:
                if pos in distances:
                    if distances[pos] > distance + 1:
                        distances[pos] = distance + 1
                else:
                    distances[pos] = distance + 1
    assert False


def main():
    year, day = 2019, 20
    data = get_data(year, day)
    print(solve_maze(data))
    print(solve_maze_recursive(data))


if __name__ == "__main__":
    main()
