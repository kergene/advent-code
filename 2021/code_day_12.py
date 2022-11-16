from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum.split('-')


def path_count(data):
    paths = defaultdict(set)
    for start, end in data:
        paths[start].add(end)
        paths[end].add(start)
    smalls = set()
    for cave in paths.keys():
        if cave.lower() == cave:
            smalls.add(cave)
    routes = set()
    routes.add(('start', ))
    route_count = 0
    while routes:
        path = list(routes.pop())
        intersections = set(path) & smalls
        cave = path[-1]
        for next_cave in paths[cave]:
            if next_cave not in intersections:
                if next_cave == 'end':
                    route_count += 1
                else:
                    routes.add(tuple(path + [next_cave]))
    return route_count


def path_count_revisiting(data):
    paths = defaultdict(set)
    for start, end in data:
        paths[start].add(end)
        paths[end].add(start)
    smalls = set()
    for cave in paths.keys():
        if cave.lower() == cave:
            smalls.add(cave)
    routes = set()
    routes.add(('start', ))
    route_count = 0
    while routes:
        path = list(routes.pop())
        intersections = set(path) & smalls
        small_paths = [cave for cave in path if cave in smalls]
        duplicate = len(small_paths) - len(set(small_paths))
        cave = path[-1]
        for next_cave in paths[cave]:
            if next_cave != 'start':
                if next_cave in intersections:
                    if not duplicate:
                        routes.add(tuple(path + [next_cave]))
                if next_cave not in intersections:
                    if next_cave == 'end':
                        route_count += 1
                    else:
                        routes.add(tuple(path + [next_cave]))
    return route_count


def main():
    year, day = 2021, 12
    data = get_data(year, day)
    print(path_count(data))
    print(path_count_revisiting(data))


if __name__ == "__main__":
    main()
