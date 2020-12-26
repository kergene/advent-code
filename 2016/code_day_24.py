from itertools import combinations, permutations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [list(datum) for datum in data]
    return data


def get_numbers(grid):
    numbers = dict()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] in '01234567':
                numbers[grid[i][j]] = (i,j)
    return numbers


def find_tsp_distances(grid):
    DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
    number_coords = get_numbers(grid)
    tsp_distances = {}
    for i, j in combinations(number_coords, r=2):
        start = number_coords[i]
        target = number_coords[j]
        q = set()
        q.add(start)
        distances = {}
        distances[start] = 0
        while q:
            x, y = choice = min(q, key=lambda x:distances[x])
            q.remove(choice)
            distance = distances[choice]
            if choice == target:
                tsp_distances[(i, j)] = distance
                tsp_distances[(j, i)] = distance
            else:
                for dx, dy in DIRECTIONS:
                    a, b = pos = x + dx, y + dy
                    if 0 <= a < len(grid) and 0 <= b < len(grid[0]):
                        if grid[a][b] != '#':
                            # can move here
                            if pos in distances:
                                if distance + 1 < distances[pos]:
                                    q.add(pos)
                                    distances[pos] = distance + 1
                            else:
                                q.add(pos)
                                distances[pos] = distance + 1
    return tsp_distances


def tsp(tsp_distances, complete_loop=True):
    min_dist = max(tsp_distances.values()) * 9 ** 9
    for ordering in permutations('1234567'):
        current = '0'
        dist = 0
        for vertex in ordering:
            dist += tsp_distances[(current, vertex)]
            current = vertex
        if complete_loop:
            dist += tsp_distances[(current, '0')]
        if dist < min_dist:
            min_dist = dist
    return min_dist


def main():
    year, day = 2016, 24
    data = get_data(year, day)
    tsp_distances = find_tsp_distances(data)
    print(tsp(tsp_distances, complete_loop=False))
    print(tsp(tsp_distances))


if __name__ == "__main__":
    main()
