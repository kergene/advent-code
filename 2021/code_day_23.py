from collections import defaultdict
from heapdict import heapdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def sort_pods(data, pod_count):
    LETTERS = 'ABCD'
    FINISH = (3, 5, 7, 9)
    FINISH = [item for item in FINISH for _ in range(pod_count)]
    locations = defaultdict(list)
    space = set()
    for r, row in enumerate(data):
        for c, cell in enumerate(row):
            if cell in LETTERS:
                locations[cell].append((r, c))
                space.add((r,c))
            elif cell == '.':
                space.add((r,c))
    locations = tuple(locations[letter][idx] for letter in LETTERS for idx in range(pod_count))
    # run dykstra
    distances = heapdict()
    distances[locations] = 0
    seens = set()
    while distances:
        choice, distance = distances.popitem()
        seens.add(choice)
        if check_finish(choice, FINISH):
            return distance
        choice = list(choice)
        location_set = set(choice)
        for position, ambipod in enumerate(choice):
            r, c = ambipod
            group = position // pod_count
            target_column = (group)*2 + 3
            blocked_positions = set(range(group*pod_count, (group + 1)*pod_count))
            other_positions = set(range(len(choice)))
            other_positions.difference_update(blocked_positions)
            if ambipod[0] != 1:
                # must move out
                # check allowed to move out first
                # 1) don't leave room if correct and no pods present (speed)
                if (not target_column == ambipod[1] or any(choice[test_pos][1] == target_column for test_pos in other_positions)):
                    new_places = move_out(ambipod, location_set, space)
                    # go through new places to add
                    for new_loc in new_places:
                        new_choice = tuple(choice[:position] + [new_loc] + choice[position + 1:])
                        new_distance = abs(r - new_loc[0]) + abs(c - new_loc[1])
                        new_distance *= 10 ** (group)
                        new_choice = map_choice(new_choice, pod_count)
                        if new_choice not in seens:
                            if new_choice in distances:
                                if distances[new_choice] > distance + new_distance:
                                    distances[new_choice] = distance + new_distance
                            else:
                                distances[new_choice] = distance + new_distance
            else:
                # must move in
                # room must be empty of other pods
                if not any(choice[test_pos][1] == target_column for test_pos in other_positions):
                    new_loc = move_in(ambipod, location_set, space, target_column)
                    # go through new places to add
                    if new_loc is not None:
                        new_choice = tuple(choice[:position] + [new_loc] + choice[position + 1:])
                        new_distance = abs(r - new_loc[0]) + abs(c - new_loc[1])
                        new_distance *= 10 ** (group)
                        new_choice = map_choice(new_choice, pod_count)
                        if new_choice not in seens:
                            if new_choice in distances:
                                if distances[new_choice] > distance + new_distance:
                                    distances[new_choice] = distance + new_distance
                            else:
                                distances[new_choice] = distance + new_distance


def map_choice(choice, pod_count):
    locations = []
    for x in range(4):
        to_add = sorted(choice[x*pod_count:(x+1)*pod_count])
        for item in to_add:
            locations.append(item)
    return tuple(locations)


def move_out(ambipod, locations, space):
    # move up and then out
    banned = set((1, x) for x in (3, 5, 7, 9))
    banned.add(ambipod)
    seens = set()
    r,c = ambipod
    broken_flag = False
    while r != 1:
        r -= 1
        new_place = r, c
        if new_place in locations:
            broken_flag = True
            r = 1
    if broken_flag:
        return set()
    for dc in (-1, 1):
        broken_flag = False
        ambipod = 1, c
        while not broken_flag:
            c += dc
            new_place = 1, c
            if new_place not in space:
                broken_flag = True
            elif new_place in locations:
                broken_flag = True
            else:
                seens.add(new_place)
    seens.difference_update(banned)
    return seens


def move_in(ambipod, locations, space, finish_column):
    # move to column and then down as far as possible
    r, c = ambipod
    broken_flag = False
    direction = 1 if finish_column > c else -1
    while c != finish_column:
        c += direction
        new_place = r, c
        if new_place in locations:
            c = finish_column
            broken_flag = True
    if broken_flag:
        return None
    broken_flag = False
    new_place = 1, finish_column
    while True:
        old_place = new_place
        r += 1
        new_place = r, finish_column
        if new_place not in space:
            return old_place
        if new_place in locations:
            return old_place


def check_finish(locations, FINISH):
    for idx in range(len(FINISH)):
        if FINISH[idx] != locations[idx][1]:
            return 0
    return 1


def sort_additional(data):
    new_rows = ['  #D#C#B#A#', '  #D#B#A#C#']
    new_data = data[:3] + new_rows + data[3:]
    return sort_pods(new_data, 4)


def main():
    year, day = 2021, 23
    data = get_data(year, day)
    print(sort_pods(data, 2))
    print(sort_additional(data))


if __name__ == "__main__":
    main()
