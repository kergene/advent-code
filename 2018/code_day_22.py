from heapdict import heapdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    depth = int(data[0].split(': ')[1])
    target = tuple(int(val) for val in  data[1].split(': ')[1].split(','))
    return depth, target


def preprocess(datum):
    return datum.split(': ')


def risk_level(depth, target):
    tot = 0
    erosion_levels = dict()
    for x in range(target[0] + 1):
        for y in range(target[1] + 1):
            if x == 0:
                geo = 48271 * y
            elif y == 0:
                geo = 16807 * x
            elif (x, y) == target:
                geo = 0
            else:
                geo = erosion_levels[x - 1, y] * erosion_levels[x, y - 1]
            ero = (geo + depth) % 20183
            erosion_levels[x, y] = ero
            tot += ero % 3
    return tot


def fastest_path(depth, target):
    # tool must be different from region
    DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
    state = 0, 0, 1
    distances = heapdict()
    seens = set()
    distances[state] = 0
    d_target = (*target, 1)
    while distances:
        state, time = distances.popitem()
        seens.add(state)
        if state == d_target:
            return time
        x, y, tool = state
        region = get_erosion_level(x, y, depth, target) % 3
        for idx in (1, 2):
            new_tool = (tool + idx) % 3
            if new_tool != region:
                new_pos = x, y, new_tool
                if new_pos not in seens:
                    if new_pos in distances:
                        if distances[new_pos] > time + 7:
                            distances[new_pos] = time + 7
                    else:
                        distances[new_pos] = time + 7
        for dx, dy in DIRECTIONS:
            a, b = x + dx, y + dy
            if 0 <= a and 0 <= b:
                new_region = get_erosion_level(a, b, depth, target) % 3
                if tool != new_region:
                    new_pos = a, b, tool
                    if new_pos not in seens:
                        if new_pos in distances:
                            if distances[new_pos] > time + 1:
                                distances[new_pos] = time + 1
                        else:
                            distances[new_pos] = time + 1
    return get_erosion_level(0, 0, depth, target) % 3


class Memoize:
    def __init__(self, func):
        self.func = func
        self.memo = dict()
    
    def __call__(self, x, y, depth, target):
        if (x, y) not in self.memo:
            self.memo[x, y] = self.func(x, y, depth, target)
        return self.memo[x, y]
        

@Memoize
def get_erosion_level(x, y, depth, target):
    if x == 0:
        geo = 48271 * y
    elif y == 0:
        geo = 16807 * x
    elif (x, y) == target:
        geo = 0
    else:
        geo = get_erosion_level(x - 1, y, depth, target) * get_erosion_level(x, y - 1, depth, target)
    return (geo + depth) % 20183


def main():
    year, day = 2018, 22
    depth, target = get_data(year, day)
    print(risk_level(depth, target))
    print(fastest_path(depth, target))


if __name__ == "__main__":
    main()
