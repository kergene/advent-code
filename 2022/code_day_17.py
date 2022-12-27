import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import import_data

def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().strip()
    return data


def part_1(jets):
    rock_type = 0
    rock_positions = {
        0: {(0,0), (0,1), (0,2), (0,3)}, # -
        1: {(0,1), (1,0), (1,1), (1,2), (2,1)}, # +
        2: {(0,0), (0,1), (0,2), (1,2), (2,2)}, # J
        3: {(0,0), (1,0), (2,0), (3,0)}, # |
        4: {(0,0), (0,1), (1,0), (1,1)} # o
    }
    jet_index = 0
    jet_count = len(jets)
    height = 0
    rocks = set()
    for col_idx in range(7):
        rocks.add((0, col_idx))
    for _ in range(2022):
        reference_row = height + 4
        reference_col = 2
        while True:
            # try to move in jet direction
            if jets[jet_index] == '>':
                for row_offset, col_offset in rock_positions[rock_type]:
                    test_row = reference_row + row_offset
                    test_col = reference_col + col_offset + 1
                    if (test_row, test_col) in rocks or test_col > 6:
                        break
                else:
                    reference_col += 1
            else:
                for row_offset, col_offset in rock_positions[rock_type]:
                    test_row = reference_row + row_offset
                    test_col = reference_col + col_offset - 1
                    if (test_row, test_col) in rocks or test_col < 0:
                        break
                else:
                    reference_col -= 1
            # increment jet_index
            jet_index += 1
            jet_index %= jet_count
            # try to move down
            can_move = True
            for row_offset, col_offset in rock_positions[rock_type]:
                test_row = reference_row + row_offset - 1
                test_col = reference_col + col_offset
                if (test_row, test_col) in rocks or test_col < 0:
                    can_move = False
                    break
            if can_move:
                reference_row -= 1
            else:
                break
        # fix rock in place
        for row_offset, col_offset in rock_positions[rock_type]:
            final_row = reference_row + row_offset
            final_col = reference_col + col_offset
            rocks.add((final_row, final_col))
            height = max(final_row, height)
        rock_type += 1
        rock_type %= 5
    return height


def find_loop(jets):
    counter = 0
    rock_type = 0
    rock_positions = {
        0: {(0,0), (0,1), (0,2), (0,3)}, # -
        1: {(0,1), (1,0), (1,1), (1,2), (2,1)}, # +
        2: {(0,0), (0,1), (0,2), (1,2), (2,2)}, # J
        3: {(0,0), (1,0), (2,0), (3,0)}, # |
        4: {(0,0), (0,1), (1,0), (1,1)} # o
    }
    jet_index = 0
    jet_count = len(jets)
    rocks = set()
    for col_idx in range(7):
        rocks.add((0, col_idx))
    loop_tracker = {}
    height = 0
    while True:
        # stop when we see a pattern where ---- must be placed
        if rock_type == 0 and (height, 3) in rocks:
            if jet_index not in loop_tracker:
                loop_tracker[jet_index] = counter, height
            else:
                old_counter, old_height = loop_tracker[jet_index]
                return old_counter, old_height, counter, height, rocks, jet_index
        if rock_type == jet_index == 0 and counter > 0:
            break
        reference_row = height + 4
        reference_col = 2
        while True:
            # try to move in jet direction
            if jets[jet_index] == '>':
                for row_offset, col_offset in rock_positions[rock_type]:
                    test_row = reference_row + row_offset
                    test_col = reference_col + col_offset + 1
                    if (test_row, test_col) in rocks or test_col > 6:
                        break
                else:
                    reference_col += 1
            else:
                for row_offset, col_offset in rock_positions[rock_type]:
                    test_row = reference_row + row_offset
                    test_col = reference_col + col_offset - 1
                    if (test_row, test_col) in rocks or test_col < 0:
                        break
                else:
                    reference_col -= 1
            # increment jet_index
            jet_index += 1
            jet_index %= jet_count
            # try to move down
            can_move = True
            for row_offset, col_offset in rock_positions[rock_type]:
                test_row = reference_row + row_offset - 1
                test_col = reference_col + col_offset
                if (test_row, test_col) in rocks or test_col < 0:
                    can_move = False
                    break
            if can_move:
                reference_row -= 1
            else:
                break
        # fix rock in place
        for row_offset, col_offset in rock_positions[rock_type]:
            final_row = reference_row + row_offset
            final_col = reference_col + col_offset
            rocks.add((final_row, final_col))
            height = max(height, final_row)
        rock_type += 1
        rock_type %= 5
        counter += 1
    assert False



def part_2(jets):
    target = 1000000000000
    # this isn't guaranteed with every input, but we look for
    # a 'nice' place to stop
    rock_positions = {
        0: {(0,0), (0,1), (0,2), (0,3)}, # -
        1: {(0,1), (1,0), (1,1), (1,2), (2,1)}, # +
        2: {(0,0), (0,1), (0,2), (1,2), (2,2)}, # J
        3: {(0,0), (1,0), (2,0), (3,0)}, # |
        4: {(0,0), (0,1), (1,0), (1,1)} # o
    }
    old_counter, old_height, mid_counter, mid_height, rocks, jet_index = find_loop(jets)
    cycle_length = mid_counter - old_counter
    height_change = mid_height - old_height
    cycle_count = (target - old_counter) // cycle_length
    rocks_remaining = (target - old_counter) % cycle_length
    # run loop one last time
    rock_type = 0
    jet_count = len(jets)
    height = mid_height
    for _ in range(rocks_remaining):
        reference_row = height + 4
        reference_col = 2
        while True:
            # try to move in jet direction
            if jets[jet_index] == '>':
                for row_offset, col_offset in rock_positions[rock_type]:
                    test_row = reference_row + row_offset
                    test_col = reference_col + col_offset + 1
                    if (test_row, test_col) in rocks or test_col > 6:
                        break
                else:
                    reference_col += 1
            else:
                for row_offset, col_offset in rock_positions[rock_type]:
                    test_row = reference_row + row_offset
                    test_col = reference_col + col_offset - 1
                    if (test_row, test_col) in rocks or test_col < 0:
                        break
                else:
                    reference_col -= 1
            # increment jet_index
            jet_index += 1
            jet_index %= jet_count
            # try to move down
            can_move = True
            for row_offset, col_offset in rock_positions[rock_type]:
                test_row = reference_row + row_offset - 1
                test_col = reference_col + col_offset
                if (test_row, test_col) in rocks or test_col < 0:
                    can_move = False
                    break
            if can_move:
                reference_row -= 1
            else:
                break
        # fix rock in place
        for row_offset, col_offset in rock_positions[rock_type]:
            final_row = reference_row + row_offset
            final_col = reference_col + col_offset
            rocks.add((final_row, final_col))
            height = max(height, final_row)
        rock_type += 1
        rock_type %= 5
    extra_height = height - mid_height
    height = old_height + height_change * cycle_count + extra_height
    return height


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
