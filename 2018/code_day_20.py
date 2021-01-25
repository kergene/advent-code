from collections import defaultdict
from heapdict import heapdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return data


def preprocess(data):
    return data


def make_graph(data):
    edges = defaultdict(set)
    vertices = set()
    states = defaultdict(set)
    idx = 0
    pos = 0, 0
    states[0].add(pos)
    depth_nodes = defaultdict(set)
    depth_indices = dict()
    depth = 0
    while True:
        step = data[idx]
        if step == '$':
            states[idx] = states[idx - 1]
            break
        elif step == '^':
            pass
        elif step == 'E':
            for old_pos in states[idx - 1]:
                x, y = old_pos
                x += 1
                new_pos = x, y
                vertices.add(new_pos)
                edges[old_pos].add(new_pos)
                edges[new_pos].add(old_pos)
                states[idx].add(new_pos)
        elif step == 'W':
            for old_pos in states[idx - 1]:
                x, y = old_pos
                x -= 1
                new_pos = x, y
                vertices.add(new_pos)
                edges[old_pos].add(new_pos)
                edges[new_pos].add(old_pos)
                states[idx].add(new_pos)
        elif step == 'N':
            for old_pos in states[idx - 1]:
                x, y = old_pos
                y += 1
                new_pos = x, y
                vertices.add(new_pos)
                edges[old_pos].add(new_pos)
                edges[new_pos].add(old_pos)
                states[idx].add(new_pos)
        elif step == 'S':
            for old_pos in states[idx - 1]:
                x, y = old_pos
                y -= 1
                new_pos = x, y
                vertices.add(new_pos)
                edges[old_pos].add(new_pos)
                edges[new_pos].add(old_pos)
                states[idx].add(new_pos)
        elif step == '(':
            depth += 1
            depth_indices[depth] = idx
            states[idx] = states[idx - 1]
        elif step == '|':
            states[idx] = states[depth_indices[depth]]
            for old_pos in states[idx - 1]:
                depth_nodes[depth].add(old_pos)
        elif step == ')':
            for old_pos in states[idx - 1]:
                depth_nodes[depth].add(old_pos)
            states[idx] = depth_nodes[depth]
            del states[depth_indices[depth]]
            del depth_nodes[depth]
            depth -= 1
        else:
            assert False, idx
        if data[idx - 1] != '(' and idx > 0:
            del states[idx - 1]
        idx += 1
    return edges


def max_path_finder(data):
    edges = make_graph(data)
    start = (0, 0)
    distances = heapdict()
    distances[start] = 0
    all_distances = dict()
    seens = set()
    while distances:
        choice, distance = distances.popitem()
        all_distances[choice] = distance
        seens.add(choice)
        for vertex in edges[choice]:
            if vertex not in seens:
                if vertex in distances:
                    if distances[vertex] > distance + 1:
                        distances[vertex] = distance + 1
                else:
                    distances[vertex] = distance + 1
    return max(all_distances.values()), all_distances


def long_path_count(distances):
    return sum(length >= 1000 for length in distances.values())


def main():
    year, day = 2018, 20
    data = get_data(year, day)
    max_distance, distances = max_path_finder(data)
    print(max_distance)
    print(long_path_count(distances))


if __name__ == "__main__":
    main()
