import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import import_data

def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return [int(val) for val in datum]


def count_seen_trees(data):
    total = 0
    for row_idx in range(len(data)):
        for col_idx in range(len(data[0])):
            tree = data[row_idx][col_idx]
            if all(tree > data[row_idx][new_col] for new_col in range(0, col_idx)):
                total += 1
            elif all(tree > data[row_idx][new_col] for new_col in range(col_idx + 1, len(data[0]))):
                total += 1
            elif all(tree > data[new_row][col_idx] for new_row in range(0, row_idx)):
                total += 1
            elif all(tree > data[new_row][col_idx] for new_row in range(row_idx + 1, len(data))):
                total += 1
    return total


def max_scenic_score(data):
    best_score = 0
    DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))
    for row_idx in range(len(data)):
        for col_idx in range(len(data[0])):
            tree = data[row_idx][col_idx]
            score = 1
            for row_diff, col_diff in DIRECTIONS:
                counter = 0
                while True:
                    counter += 1
                    if not 0 <= col_idx + counter * col_diff < len(data[0]):
                        counter -= 1
                        break
                    if not 0 <= row_idx + counter * row_diff < len(data):
                        counter -= 1
                        break
                    new_tree = data[row_idx + counter * row_diff][col_idx + counter * col_diff]
                    if new_tree >= tree:
                        break
                score *= counter
            if score > best_score:
                best_score = score
    return best_score


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(count_seen_trees(data))
    print(max_scenic_score(data))


if __name__ == "__main__":
    main()
