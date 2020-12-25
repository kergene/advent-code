from itertools import permutations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    paths = dict(create_paths(path) for path in data)
    return paths


def create_paths(path):
    path = path.split()
    return ((path[0], path[2]), int(path[4]))


def get_dist(ordering, paths):
    return sum(find_length(ordering[i:i+2], paths) for i in range(len(ordering) - 1))


def find_length(ordering, paths):
    if (ordering[0], ordering[1]) in paths:
        return paths[(ordering[0], ordering[1])]
    else:
        return paths[(ordering[1], ordering[0])]


def shortest_route(paths):
    locations = set()
    for i, j in paths.keys():
        locations.add(i)
        locations.add(j)
    best_dist = max(paths.values())*len(locations)
    for ordering in permutations(locations, len(locations)):
        new_dist = get_dist(ordering, paths)
        if new_dist < best_dist:
            best_dist = new_dist
    return best_dist


def longest_route(paths):
    locations = set()
    for i, j in paths.keys():
        locations.add(i)
        locations.add(j)
    best_dist = 0
    for ordering in permutations(locations, len(locations)):
        new_dist = get_dist(ordering, paths)
        if new_dist > best_dist:
            best_dist = new_dist
    return best_dist


def main():
    year, day = 2015, 9
    paths = get_data(year, day)
    print(shortest_route(paths))
    print(longest_route(paths))


if __name__ == "__main__":
    main()
