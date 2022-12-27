import sys
from pathlib import Path
from collections import Counter
from collections import defaultdict

sys.path.append(str(Path(__file__).parent.parent))
import import_data


def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().strip()
    return data


def find_start_markers_old(data, bits):
    # initial, slower implementation, retained for conciseness
    for idx in range(len(data) - bits + 1):
        # could also use len(set(X)) == len(X)
        if max(Counter(data[idx:idx+bits]).values()) == 1:
            return idx+bits


def find_start_markers(data, bits):
    # faster implementation using sliding window and hashmap
    duplicate_counter = 0
    count_dict = defaultdict(int)
    # add first bits to hashmap
    for idx in range(bits):
        new_bit = data[idx]
        count_dict[new_bit] += 1
        if count_dict[new_bit] == 2:
            duplicate_counter += 1
    tracking_idx = bits
    while bits < len(data):
        # move sliding window until no duplicates
        if duplicate_counter == 0:
            return tracking_idx
        old_bit = data[tracking_idx - bits]
        new_bit = data[tracking_idx]
        count_dict[old_bit] -= 1
        if count_dict[old_bit] == 1:
            duplicate_counter -= 1
        count_dict[new_bit] += 1
        if count_dict[new_bit] == 2:
            duplicate_counter += 1
        tracking_idx += 1


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(find_start_markers(data, 4))
    print(find_start_markers(data, 14))


if __name__ == "__main__":
    main()
