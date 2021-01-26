from heapdict import heapdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return tuple(int(val) for val in datum.split('/'))


def strongest_bridge(data):
    n = len(data)
    starts = [idx for idx in range(n) if 0 in data[idx]]
    lengths = heapdict()
    for idx in starts:
        used_components = [0] * n
        used_components[idx] = 1
        score = sum(data[idx])
        lengths[tuple(used_components)] = score, score
    while lengths:
        choice, details = lengths.popitem()
        score, next_val = details
        for missing_idx in range(n):
            if choice[missing_idx] == 0:
                if next_val in data[missing_idx]:
                    # can add component
                    next_choice = list(choice)
                    next_choice[missing_idx] = 1
                    next_choice = tuple(next_choice)
                    new_score = sum(data[missing_idx])
                    lengths[next_choice] = score + new_score, new_score - next_val
    return score


def longest_bridge(data):
    n = len(data)
    starts = [idx for idx in range(n) if 0 in data[idx]]
    lengths = heapdict()
    for idx in starts:
        used_components = [0] * n
        used_components[idx] = 1
        score = sum(data[idx])
        lengths[tuple(used_components)] = 1, score, score
    while lengths:
        choice, details = lengths.popitem()
        length, score, next_val = details
        for missing_idx in range(n):
            if choice[missing_idx] == 0:
                if next_val in data[missing_idx]:
                    # can add component
                    next_choice = list(choice)
                    next_choice[missing_idx] = 1
                    next_choice = tuple(next_choice)
                    new_score = sum(data[missing_idx])
                    lengths[next_choice] = length + 1, score + new_score, new_score - next_val
    return score


def main():
    year, day = 2017, 24
    data = get_data(year, day)
    print(strongest_bridge(data))
    print(longest_bridge(data))


if __name__ == "__main__":
    main()
