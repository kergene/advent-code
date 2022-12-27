import sys
from pathlib import Path
from queue import LifoQueue

sys.path.append(str(Path(__file__).parent.parent))
import import_data

def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = datum.split(' -> ')
    datum = [[int(val) for val in pair.split(',')] for pair in datum]
    return datum


def sand_at_rest(data):
    walls = set()
    for row in data:
        for idx in range(len(row) - 1):
            curr_x, curr_y = row[idx]
            next_x, next_y = row[idx + 1]
            if curr_x == next_x:
                min_y = min(curr_y, next_y)
                max_y = max(curr_y, next_y)
                for new_y in range(min_y, max_y + 1):
                    walls.add((curr_x, new_y))
            elif curr_y == next_y:
                min_x = min(curr_x, next_x)
                max_x = max(curr_x, next_x)
                for new_x in range(min_x, max_x + 1):
                    walls.add((new_x, curr_y))
    return create_sand(walls)


def create_sand(walls):
    sand_count = 0
    sand_x, sand_y = 500, 0
    sand_queue = LifoQueue()
    while True:
        if sand_y > max(wall[1] for wall in walls):
            return sand_count
        if (sand_x, sand_y + 1) not in walls:
            sand_queue.put((sand_x, sand_y))
            sand_y += 1
        elif (sand_x - 1, sand_y + 1) not in walls:
            sand_queue.put((sand_x, sand_y))
            sand_x -= 1
            sand_y += 1
        elif (sand_x + 1, sand_y + 1) not in walls:
            sand_queue.put((sand_x, sand_y))
            sand_x += 1
            sand_y += 1
        else:
            walls.add((sand_x, sand_y))
            sand_count += 1
            sand_x, sand_y = sand_queue.get()


def sand_at_rest_floored(data):
    walls = set()
    for row in data:
        for idx in range(len(row) - 1):
            curr_x, curr_y = row[idx]
            next_x, next_y = row[idx + 1]
            if curr_x == next_x:
                min_y = min(curr_y, next_y)
                max_y = max(curr_y, next_y)
                for new_y in range(min_y, max_y + 1):
                    walls.add((curr_x, new_y))
            elif curr_y == next_y:
                min_x = min(curr_x, next_x)
                max_x = max(curr_x, next_x)
                for new_x in range(min_x, max_x + 1):
                    walls.add((new_x, curr_y))
    return create_more_sand(walls)


def create_more_sand(walls):
    sand_count = 0
    sand_x, sand_y = 500, 0
    max_y = max(wall[1] for wall in walls) + 1
    sand_queue = LifoQueue()
    while True:
        if sand_y == max_y:
            walls.add((sand_x, sand_y))
            sand_count += 1
            sand_x, sand_y = sand_queue.get()
        if (sand_x, sand_y + 1) not in walls:
            sand_queue.put((sand_x, sand_y))
            sand_y += 1
        elif (sand_x - 1, sand_y + 1) not in walls:
            sand_queue.put((sand_x, sand_y))
            sand_x -= 1
            sand_y += 1
        elif (sand_x + 1, sand_y + 1) not in walls:
            sand_queue.put((sand_x, sand_y))
            sand_x += 1
            sand_y += 1
        else:
            walls.add((sand_x, sand_y))
            sand_count += 1
            if (sand_x, sand_y) == (500, 0):
                return sand_count
            sand_x, sand_y = sand_queue.get()


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(sand_at_rest(data))
    print(sand_at_rest_floored(data))


if __name__ == "__main__":
    main()
