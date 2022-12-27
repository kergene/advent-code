import sys
from pathlib import Path
from math import prod

sys.path.append(str(Path(__file__).parent.parent))
import import_data


def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().split('\n\n')
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = datum.splitlines()
    return [evaluate_packet(packet, 1)[0] for packet in datum]


def evaluate_packet(raw_packet, index):
    new_packet = []
    int_chars = []
    while index < len(raw_packet):
        character = raw_packet[index]
        index += 1
        if character == '[':
            temp_packet, index = evaluate_packet(raw_packet, index)
            new_packet.append(temp_packet)
        elif character == ',':
            if len(int_chars) > 0:
                new_int = int(''.join(int_chars))
                new_packet.append(new_int)
                int_chars = []
        elif character == ']':
            if len(int_chars) > 0:
                new_int = int(''.join(int_chars))
                new_packet.append(new_int)
                int_chars = []
            return new_packet, index
        else:
            int_chars.append(character)
    assert False


def test_pairs(data):
    total = 0
    for idx, row in enumerate(data):
        left, right = row
        if compare_packets(left, right) < 0:
            total += idx + 1
    return total


def compare_packets(left, right):
    if isinstance(left, list) and isinstance(right, list):
        if len(left) == 0 and len(right) == 0:
            return 0
        if len(left) == 0:
            return -1
        if len(right) == 0:
            return 1
        score = compare_packets(left[0], right[0])
        if score == 0:
            return compare_packets(left[1:], right[1:])
        return score
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        if left > right:
            return 1
        return 0
    if isinstance(left, int) and isinstance(right, list):
        return compare_packets([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return compare_packets(left, [right])
    assert False


def sort_packets(data):
    # start at [1, 2] to include counts
    scores = [1, 2]
    divs = [[[2]], [[6]]]
    for row in data:
        for item in row:
            for idx in range(len(divs)):
                if compare_packets(item, divs[idx]) < 0:
                    scores[idx] += 1
    return prod(scores)


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(test_pairs(data))
    print(sort_packets(data))


if __name__ == "__main__":
    main()
