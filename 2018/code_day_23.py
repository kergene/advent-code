from heapdict import heapdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    data = (
        data.replace('<', '(')
            .replace('>', ')')
            .replace('=', ':')
            .replace('\n', '}, {')
            .replace('pos', "'pos'")
            .replace('r', "'r'")
    )
    data = ''.join(['{', data, '}'])
    data = eval(data)
    return data


def strongest_node(data):
    max_node = max(data, key=lambda x: x['r'])
    r = max_node['r']
    pos = max_node['pos']
    count = 0
    for other_node in data:
        other_pos = other_node['pos']
        if manhattan_distance(pos, other_pos) <= r:
            count += 1
    return count


def manhattan_distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def strongest_point(data):
    EIGHT_SPLIT = (
        (0, 0, 0), (0, 0, 1),
        (0, 1, 0), (0, 1, 1),
        (1, 0, 0), (1, 0, 1),
        (1, 1, 0), (1, 1, 1)
    )
    ORIGIN = (0, 0, 0)
    max_dim = max(abs(pos) for node in data for pos in node['pos'])
    size = 1
    while size < max_dim:
        size *= 2
    box = ((-size, -size, -size), (size, size, size))
    heap = heapdict()
    node = (-len(data), -2 * size, 3 * size)
    # number of bots, size negated
    heap[box] = node
    while heap:
        choice, details = heap.popitem()
        _, box_size, closeness = details
        if box_size == -1:
            return closeness
        else:
            box_size //= 2
            for corner in EIGHT_SPLIT:
                new_box_min = tuple(choice[0][idx] - box_size * corner[idx] for idx in range(3))
                new_box_max = tuple(val - box_size for val in new_box_min)
                new_box = (new_box_min, new_box_max)
                heap[new_box] = (-count_intercepts(new_box, data), box_size, manhattan_distance(new_box_min, ORIGIN))


def count_intercepts(box, data):
    return sum(box_and_node_intercept(box, node) for node in data)


def box_and_node_intercept(box, node):
    pos = node['pos']
    r = node['r']
    box_min = box[0]
    box_max = tuple(val - 1 for val in box[1])
    d = (
        manhattan_distance(box_max, pos)
        + manhattan_distance(box_min, pos)
        - manhattan_distance(box_max, box_min)
    )
    d //= 2
    return d <= r


def main():
    year, day = 2018, 23
    data = get_data(year, day)
    print(strongest_node(data))
    print(strongest_point(data))


if __name__ == "__main__":
    main()
