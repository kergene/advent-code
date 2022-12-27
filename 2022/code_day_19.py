import sys
from pathlib import Path
from queue import SimpleQueue

sys.path.append(str(Path(__file__).parent.parent))
import import_data

def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    blueprint, components = datum.split(': ')
    blueprint = int(blueprint.split()[1])
    components = components[:-1].split('. ')
    ore_ore = int(components[0].split()[-2])
    clay_ore = int(components[1].split()[-2])
    obsidian_ore = int(components[2].split()[-5])
    obsidian_clay = int(components[2].split()[-2])
    geode_ore = int(components[3].split()[-5])
    geode_obsidian = int(components[3].split()[-2])
    return (
        blueprint,
        (ore_ore, 0, 0),
        (clay_ore, 0, 0),
        (obsidian_ore, obsidian_clay, 0),
        (geode_ore, 0, geode_obsidian)
    )


def run_requirements_queue(requirements, total_mins):
    max_robots = tuple(max(x) for x in zip(*requirements))
    robots = (1, 0, 0, 0)
    rocks = (0, 0, 0, 0)
    minutes = 0
    seens = set()
    queue = SimpleQueue()
    state = ((robots, rocks), minutes)
    queue.put(state)
    best_geode = 0
    while not queue.empty():
        choice, minutes = queue.get()
        robots, rocks = choice
        new_minutes = minutes + 1
        # try adding non-geode robot (don't bother unless minutes < 21)
        if minutes < total_mins - 3:
            for robot_idx in range(3):
                # don't try if already have most robots we could need
                if robots[robot_idx] < max_robots[robot_idx]:
                    if all(rocks[req_idx] >= requirements[robot_idx][req_idx] for req_idx in range(4)):
                        # can add robot
                        new_rocks = [rocks[rock_idx] - requirements[robot_idx][rock_idx] + robots[rock_idx] for rock_idx in range(4)]
                        new_robots = list(robots)
                        new_robots[robot_idx] += 1
                        new_robots = tuple(new_robots)
                        mins_remaining = total_mins - new_minutes
                        max_rocks = [max_robots[rock_idx] + (max_robots[rock_idx] - robots[rock_idx]) * (mins_remaining - 1) for rock_idx in range(4)]
                        max_rocks[3] = total_mins ** 2
                        new_rocks = tuple(min(max_rocks[rock_idx], new_rocks[rock_idx]) for rock_idx in range(4))
                        new_choice = new_robots, new_rocks
                        if new_choice not in seens:
                            seens.add(new_choice)
                            queue.put((new_choice, new_minutes))
        # try adding geode robot (don't bother if it's the last minute)
        if minutes < total_mins - 1:
            robot_idx = 3
            if all(rocks[req_idx] >= requirements[robot_idx][req_idx] for req_idx in range(4)):
                # can add robot
                new_rocks = [rocks[rock_idx] - requirements[robot_idx][rock_idx] + robots[rock_idx] for rock_idx in range(4)]
                new_robots = list(robots)
                new_robots[robot_idx] += 1
                new_robots = tuple(new_robots)
                mins_remaining = total_mins - new_minutes
                max_rocks = [max_robots[rock_idx] + (max_robots[rock_idx] - robots[rock_idx]) * (mins_remaining - 1) for rock_idx in range(4)]
                max_rocks[3] = total_mins ** 2
                new_rocks = tuple(min(max_rocks[rock_idx], new_rocks[rock_idx]) for rock_idx in range(4))
                new_choice = new_robots, new_rocks
                if new_choice not in seens:
                    seens.add(new_choice)
                    queue.put((new_choice, new_minutes))
        # also consider doing nothing
        if minutes < total_mins:
            new_rocks = tuple(rocks[rock_idx] + robots[rock_idx] for rock_idx in range(4))
            new_choice = robots, new_rocks
            if new_choice not in seens:
                seens.add(new_choice)
                queue.put((new_choice, new_minutes))
        # if 24 minutes passed, get score
        else:
            if best_geode < rocks[-1]:
                best_geode = rocks[-1]
    return best_geode


def run_requirements_queue_no_geodes(requirements, total_mins):
    max_robots = tuple(max(x) for x in zip(*requirements))
    robots = (1, 0, 0)
    rocks = (0, 0, 0)
    minutes = 0
    seens = set()
    queue = SimpleQueue()
    geodes = 0
    state = ((robots, rocks, geodes), minutes)
    queue.put(state)
    best_geode = 0
    while not queue.empty():
        choice, minutes = queue.get()
        robots, rocks, geodes = choice
        new_minutes = minutes + 1
        mins_remaining = total_mins - new_minutes
        max_extra_geodes = mins_remaining * (mins_remaining + 1) // 2
        # only continue if we can beat it
        if geodes + max_extra_geodes > best_geode:
            # try adding non-geode robot (don't bother unless minutes < 21)
            if minutes < total_mins - 3:
                for robot_idx in range(3):
                    # don't try if already have most robots we could need
                    if robots[robot_idx] < max_robots[robot_idx]:
                        if all(rocks[req_idx] >= requirements[robot_idx][req_idx] for req_idx in range(3)):
                            # can add robot
                            new_rocks = [rocks[rock_idx] - requirements[robot_idx][rock_idx] + robots[rock_idx] for rock_idx in range(3)]
                            new_robots = list(robots)
                            new_robots[robot_idx] += 1
                            new_robots = tuple(new_robots)
                            max_rocks = [max_robots[rock_idx] + (max_robots[rock_idx] - robots[rock_idx]) * (mins_remaining - 1) for rock_idx in range(3)]
                            new_rocks = tuple(min(max_rocks[rock_idx], new_rocks[rock_idx]) for rock_idx in range(3))
                            new_choice = new_robots, new_rocks, geodes
                            if new_choice not in seens:
                                seens.add(new_choice)
                                queue.put((new_choice, new_minutes))
            # try adding geode robot (don't bother if it's the last minute)
            if minutes < total_mins - 1:
                robot_idx = 3
                if all(rocks[req_idx] >= requirements[robot_idx][req_idx] for req_idx in range(3)):
                    # can add robot
                    new_rocks = [rocks[rock_idx] - requirements[robot_idx][rock_idx] + robots[rock_idx] for rock_idx in range(3)]
                    max_rocks = [max_robots[rock_idx] + (max_robots[rock_idx] - robots[rock_idx]) * (mins_remaining - 1) for rock_idx in range(3)]
                    new_rocks = tuple(min(max_rocks[rock_idx], new_rocks[rock_idx]) for rock_idx in range(3))
                    new_geodes = geodes + mins_remaining
                    if best_geode < new_geodes:
                        best_geode = new_geodes
                    new_choice = robots, new_rocks, new_geodes
                    if new_choice not in seens:
                        seens.add(new_choice)
                        queue.put((new_choice, new_minutes))
            # also consider doing nothing
            if minutes < total_mins:
                new_rocks = tuple(rocks[rock_idx] + robots[rock_idx] for rock_idx in range(3))
                new_choice = robots, new_rocks, geodes
                if new_choice not in seens:
                    seens.add(new_choice)
                    queue.put((new_choice, new_minutes))
            # if 24 minutes passed, nothing happens
    return best_geode


def part_1(data):
    total = 0
    for blueprint, *requirements in data:
        # reqs are for ore, clay, obsidian, geode
        geode_score = run_requirements_queue_no_geodes(requirements, 24)
        total += blueprint * geode_score
    return total


def part_2(data):
    total = 1
    for _, *requirements in data[:3]:
        geode_score = run_requirements_queue_no_geodes(requirements, 32)
        total *= geode_score
    return total


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
