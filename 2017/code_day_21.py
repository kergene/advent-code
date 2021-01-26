def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = dict(preprocess(datum) for datum in data)
    data = all_states(data)
    return data


def all_states(data):
    # very manual
    new_states = dict()
    for key, value in data.items():
        if len(key) == 5:
            a, b, _, c, d = key
            state = [a, b, '/', c, d]
            new_states[''.join(state)] = value
            state = [b, d, '/', a, c]
            new_states[''.join(state)] = value
            state = [d, c, '/', b, a]
            new_states[''.join(state)] = value
            state = [c, a, '/', d, b]
            new_states[''.join(state)] = value
        else:
            a, b, c, _, d, e, f, _, g, h, i = key
            state = [a, b, c, '/', d, e, f, '/', g, h, i]
            new_states[''.join(state)] = value
            state = [c, f, i, '/', b, e, h, '/', a, d, g]
            new_states[''.join(state)] = value
            state = [i, h, g, '/', f, e, d, '/', c, b, a]
            new_states[''.join(state)] = value
            state = [g, d, a, '/', h, e, b, '/', i, f, c]
            new_states[''.join(state)] = value
            state = [c, b, a, '/', f, e, d, '/', i, h, g]
            new_states[''.join(state)] = value
            state = [i, f, c, '/', h, e, b, '/', g, d, a]
            new_states[''.join(state)] = value
            state = [g, h, i, '/', d, e, f, '/', a, b, c]
            new_states[''.join(state)] = value
            state = [a, d, g, '/', b, e, h, '/', c, f, i]
            new_states[''.join(state)] = value
    return new_states


def preprocess(datum):
    return tuple(datum.split(' => '))


def enhance(data):
    state = '.#./..#/###'
    state = state.split('/')
    for _ in range(5):
        state = modify_state(state, data)
    first = count_on(state)
    for _ in range(18 - 5):
        state = modify_state(state, data) 
    second = count_on(state)
    return first, second


def modify_state(state, data):
    n = 2 if len(state) % 2 == 0 else 3
    k = len(state) // n
    splits = [['.' for _ in range(k)] for _ in range(k)]
    for r in range(k):
        for c in range(k):
            old = []
            for split in range(n):
                old.append(state[r*n + split][c*n:c*n + n])
            old = '/'.join(old)
            splits[r][c] = data[old].split('/')
    new_state = []
    for r in range(k):
        for sub_r in range(n + 1):
            new = []
            for c in range(k):
                new.append(splits[r][c][sub_r])
            new_state.append(''.join(new))
    return new_state


def count_on(state):
    total = 0
    for row in state:
        total += row.count('#')
    return total


def main():
    year, day = 2017, 21
    data = get_data(year, day)
    depth_5, depth_18 = enhance(data)
    print(depth_5)
    print(depth_18)


if __name__ == "__main__":
    main()
