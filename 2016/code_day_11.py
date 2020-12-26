from itertools import combinations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    things = set(item[:-2] for floor in data for item in floor)
    i = 0
    conversion_dict = {}
    for item in things:
        conversion_dict[item] = 2*i + 1
        i += 1
    for i in range(len(data)):
        data[i] = set(conversion_dict[item[:-2]] if item[-1] == 'M' else conversion_dict[item[:-2]] + 1 for item in data[i])
    locations = [0] * 2 * len(conversion_dict)
    for i in range(len(data)):
        for item in data[i]:
            locations[item - 1] = i
    locations.append(0)
    return locations # micro, gen, micro, gen, ..., micro, gen, elevator


def preprocess(datum):
    datum = datum.split()
    datum = [i.replace(',', '').replace('.', '') for i in datum]
    generators = set(datum[i-1] + '_G' for i in range(len(datum)) if datum[i] == 'generator')
    microchips = set(datum[i-1].split('-')[0] + '_M' for i in range(len(datum)) if datum[i] == 'microchip')
    return set(generators) | set(microchips)


def one_or_two(possibles):
    for i in combinations(possibles, 1):
        yield i
    for i, j in combinations(possibles, 2):
        yield i, j


def take_step(states, seen):
    new_states = set()
    solved = False
    for locations in states:
        seen.add(locations)
        current_floor = locations[-1]
        possibles = [i for i in range(len(locations) - 1) if locations[i] == current_floor]
        for vals in one_or_two(possibles):
            if current_floor != 0:
                # move down
                new_locations = list(locations[:-1])
                for item in vals:
                    new_locations[item] -= 1
                if check_valid(new_locations):
                    new_locations.append(current_floor - 1)
                    new_locations = get_state(new_locations)
                    if new_locations not in seen:
                        new_states.add(new_locations)
                        if check_solved(new_locations):
                            return True, set(), set()
            if current_floor != 3:
                # move up
                new_locations = list(locations[:-1])
                for item in vals:
                    new_locations[item] += 1
                if check_valid(new_locations):
                    new_locations.append(current_floor + 1)
                    new_locations = get_state(new_locations)
                    if new_locations not in seen:
                        new_states.add(new_locations)
                        if check_solved(new_locations):
                            return True, set(), set()
    return solved, new_states, seen


def get_state(locations):
    # we do this because we don't care which pairs of items are which 
    # states are equivalent if have same set of pairs (and same floor)
    pairs = [(locations[i],locations[i + 1]) for i in range(0, len(locations) - 1, 2)]
    state = [item for pair in sorted(pairs) for item in pair]
    state.append(locations[-1])
    return tuple(state)


def check_valid(locations):
    for floor in range(4):
        micros = [i for i in range(len(locations)) if locations[i] == floor and i % 2 == 0]
        gens = [i - 1 for i in range(len(locations)) if locations[i] == floor and i % 2 == 1]
        if len(micros) * len(gens):
            # only may have problem if both > 0
            for item in micros:
                if item not in gens:
                    return False
    return True


def check_solved(locations):
    return all(floor == 3 for floor in locations)


def run_bfs_elevator(locations):
    locations = tuple(locations)
    states = set()
    seen = set()
    states.add(locations)
    solved = False
    steps = 0
    while not solved:
        steps += 1
        solved, states, seen = take_step(states, seen)
    return steps


def extra_items(locations):
    for _ in range(4):
        locations.append(0)
    return run_bfs_elevator(locations)


def main():
    year, day = 2016, 11
    locations = get_data(year, day)
    print(run_bfs_elevator(locations))
    print(extra_items(locations))


if __name__ == "__main__":
    main()
