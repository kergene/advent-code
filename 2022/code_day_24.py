import sys
from pathlib import Path
from queue import SimpleQueue

sys.path.append(str(Path(__file__).parent.parent))
import import_data

class Memoize:
    def __init__(self, func):
        self.func = func
        self.memo = {}

    def __call__(self, state, *data):
        if state not in self.memo:
            self.memo[state] = self.func(state, *data)
        return self.memo[state]

    def clear(self):
        self.memo.clear()


def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    data = preprocess_grid(data)
    return data


def preprocess_grid(data):
    grid = set()
    blizzards = {}
    for row_idx, row in enumerate(data):
        for col_idx, val in enumerate(row):
            if val in '.<>^v':
                grid.add((row_idx, col_idx))
                if val != '.':
                    blizzards[row_idx, col_idx] = val
    return grid, blizzards


def part_1(data):
    return run_search(data, 0, True)


def part_2(data):
    mins_out = run_search(data, 0, True)
    mins_back = run_search(data, mins_out, False)
    total_mins = run_search(data, mins_back, True)
    return total_mins


@Memoize
def get_positions(mins, blizzards):
    MOVES = {
        '^': (-1, 0),
        'v': (1, 0),
        '>': (0, 1),
        '<': (0, -1)
    }
    new_blizzards = {}
    for pos, bliz_type in blizzards.items():
        row_idx, col_idx = pos
        row_diff, col_diff = MOVES[bliz_type]
        row_idx -= 1
        row_idx += mins * row_diff
        row_idx %= 35
        row_idx += 1
        col_idx -= 1
        col_idx += mins * col_diff
        col_idx %= 100
        col_idx += 1
        new_blizzards[row_idx, col_idx] = bliz_type
    return new_blizzards


def run_search(data, mins_start, forward):
    MOVES = (
        (1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)
    )
    grid, blizzards = data
    if forward:
        start = min(grid)
        end = max(grid)
    else:
        start = max(grid)
        end = min(grid)
    queue = SimpleQueue()
    seens = set()
    queue.put((start, mins_start))
    while queue:
        state = pos, mins = queue.get()
        if pos == end:
            return mins
        row_idx, col_idx = pos
        next_blizzards = get_positions(mins + 1, blizzards)
        for row_diff, col_diff in MOVES:
            test_pos = row_idx + row_diff, col_idx + col_diff
            if test_pos in grid and test_pos not in next_blizzards.keys():
                state = (test_pos, mins + 1)
                if state not in seens:
                    queue.put(state)
                    seens.add(state)


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
