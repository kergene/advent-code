import sys
from pathlib import Path
from heapdict import heapdict

sys.path.append(str(Path(__file__).parent.parent))
import import_data

def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    return data


def short_climb(data):
    end = (0,0)
    states = heapdict()
    data_dict = dict()
    for row_idx in range(len(data)):
        for col_idx in range(len(data[0])):
            if data[row_idx][col_idx] == 'S':
                states[row_idx, col_idx] = 0
                data_dict[row_idx, col_idx] = ord('a')
            elif data[row_idx][col_idx] == 'E':
                end = (row_idx, col_idx)
                data_dict[row_idx, col_idx] = ord('z')
            else:
                data_dict[row_idx, col_idx] = ord(data[row_idx][col_idx])
    return run_dijkstra(states, end, data_dict)


def scenic_hike(data):
    end = (0, 0)
    states = heapdict()
    data_dict = dict()
    for row_idx in range(len(data)):
        for col_idx in range(len(data[0])):
            if data[row_idx][col_idx] == 'S':
                data_dict[row_idx, col_idx] = ord('a')
            elif data[row_idx][col_idx] == 'E':
                end = (row_idx, col_idx)
                data_dict[row_idx, col_idx] = ord('z')
            elif data[row_idx][col_idx] == 'a':
                states[row_idx, col_idx] = 0
                data_dict[row_idx, col_idx] = ord('a')
            else:
                data_dict[row_idx, col_idx] = ord(data[row_idx][col_idx])
    return run_dijkstra(states, end, data_dict)


def run_dijkstra(states, end, data_dict):
    DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
    seens = set()
    while states:
        choice, dist = states.popitem()
        seens.add(choice)
        if choice == end:
            return dist
        row_idx, col_idx = choice
        for row_offset, col_offset in DIRECTIONS:
            new_choice = row_idx + row_offset, col_idx + col_offset
            if new_choice not in seens and new_choice in data_dict:
                if data_dict[new_choice] - data_dict[choice] <= 1:
                    new_dist = dist + 1
                    if new_choice not in states:
                        states[new_choice] = new_dist
                    elif new_dist < states[new_choice]:
                        states[new_choice] = new_dist


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(short_climb(data))
    print(scenic_hike(data))


if __name__ == "__main__":
    main()
