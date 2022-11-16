from itertools import product
from itertools import combinations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    scanners = datum.splitlines()[1:]
    return set(tuple(int(val) for val in row.split(',')) for row in scanners)


def check_overlap(a_beacons, b_beacons):
    tries = 0
    for _ in range(3):
        for _ in range(4):
            for _ in range(2):
                tries += 1
                for a_beacon, b_beacon in product(a_beacons, b_beacons):
                    offset = tuple(a_beacon[idx] - b_beacon[idx] for idx in range(3))
                    adjusted_beacons = set()
                    for beacon in b_beacons:
                        new_beacon = tuple(beacon[idx] + offset[idx] for idx in range(3))
                        adjusted_beacons.add(new_beacon)
                    if len(a_beacons & adjusted_beacons) >= 12:
                        return True, adjusted_beacons, offset
                b_beacons = set((-beacon[0], -beacon[1], beacon[2]) for beacon in b_beacons)
            b_beacons = set((beacon[0], beacon[2], -beacon[1]) for beacon in b_beacons)
        b_beacons = set((beacon[1], beacon[2], beacon[0]) for beacon in b_beacons)
    return False, None, None


def dist(x, y):
    return sum(abs(x[idx] - y[idx]) for idx in range(3))


def find_scanners(data):
    matched = set()
    matched.add(0)
    unmatched = set(range(1,len(data)))
    sensors = {}
    sensors[0] = (0, 0, 0)
    while unmatched:
        new_matches = set()
        i = matched.pop()
        for j in unmatched:
            score, new_beacons, sensor = check_overlap(data[i], data[j])
            if score:
                data[j] = new_beacons
                sensors[j] = sensor
                new_matches.add(j)
        matched.update(new_matches)
        unmatched.difference_update(new_matches)
    total_set = set()
    for row in data:
        total_set.update(row)
    max_dist = 0
    for sensor_a, sensor_b in combinations(sensors.values(), 2):
        d = dist(sensor_a, sensor_b)
        if d > max_dist:
            max_dist = d
    return len(total_set), max_dist


def main():
    year, day = 2021, 19
    data = get_data(year, day)
    beacon_count, scanner_distance = find_scanners(data)
    print(beacon_count)
    print(scanner_distance)


if __name__ == "__main__":
    main()
