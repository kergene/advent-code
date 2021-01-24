def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = dict(preprocess(datum) for datum in data)
    return data


def preprocess(datum):
    return tuple(int(val) for val in datum.split(': '))


def severity_score(data):
    severity = 0
    for layer_depth, layer_range in data.items():
        if layer_depth % (2 * layer_range - 2) == 0:
            severity += layer_range * layer_depth
    return severity


def evade_detection(data):
    least_wait = 0
    while True:
        if any((layer_depth + least_wait) % (2 * layer_range - 2) == 0 for layer_depth, layer_range in data.items()):
            least_wait += 1
        else:
            break
    return least_wait


def main():
    year, day = 2017, 13
    data = get_data(year, day)
    print(severity_score(data))
    print(evade_detection(data))


if __name__ == "__main__":
    main()
