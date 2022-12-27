import sys
from pathlib import Path
from queue import SimpleQueue
from collections import defaultdict
from itertools import product

sys.path.append(str(Path(__file__).parent.parent))
import import_data


def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = datum.split()
    sensor_x = int(datum[2][2:-1])
    sensor_y = int(datum[3][2:-1])
    beacon_x = int(datum[8][2:-1])
    beacon_y = int(datum[9][2:])
    return ((sensor_x, sensor_y), (beacon_x, beacon_y))


def part_1(data):
    row = 2000000
    beacons = set()
    endpoints = set()
    for sensor, beacon in data:
        beacons.add(beacon)
        exclusion_distance = manhatten_distance(sensor, beacon)
        distance_to_row = abs(row - sensor[1])
        if distance_to_row <= exclusion_distance:
            buffer = exclusion_distance - distance_to_row
            range_vals = sensor[0] - buffer, sensor[0] + buffer
            endpoints.add(range_vals)
    total_length = 0
    endpoints = sorted(endpoints)
    endpoints_queue = SimpleQueue()
    for endpoint in endpoints:
        endpoints_queue.put(endpoint)
    base_endpoint = None
    while not endpoints_queue.empty():
        if base_endpoint is None:
            base_endpoint = endpoints_queue.get()
        if not endpoints_queue.empty():
            choice = endpoints_queue.get()
            if is_overlap(base_endpoint, choice):
                base_endpoint = get_overlap(base_endpoint, choice)
            else:
                total_length += base_endpoint[1] - base_endpoint[0] + 1
                base_endpoint = choice
    if base_endpoint is not None:
        total_length += base_endpoint[1] - base_endpoint[0] + 1
    for beacon in beacons:
        if beacon[1] == row:
            total_length -= 1
    return total_length


def part_2(data):
    # original (but slow) attempt making use of part 1
    bounds = 4000000
    beacons = set()
    sensor_distances = dict()
    for sensor, beacon in data:
        beacons.add(beacon)
        exclusion_distance = manhatten_distance(sensor, beacon)
        sensor_distances[sensor] = exclusion_distance
    for row in range(bounds + 1):
        endpoints = set()
        for sensor, exclusion_distance in sensor_distances.items():
            distance_to_row = abs(row - sensor[1])
            if distance_to_row <= exclusion_distance:
                buffer = exclusion_distance - distance_to_row
                range_vals = sensor[0] - buffer, sensor[0] + buffer
                endpoints.add(range_vals)
        endpoints = sorted(endpoints)
        endpoints_queue = SimpleQueue()
        for endpoint in endpoints:
            endpoints_queue.put(endpoint)
        split_endpoints = list()
        base_endpoint = None
        while not endpoints_queue.empty():
            if base_endpoint is None:
                base_endpoint = endpoints_queue.get()
            if not endpoints_queue.empty():
                choice = endpoints_queue.get()
                if is_overlap(base_endpoint, choice):
                    base_endpoint = get_overlap(base_endpoint, choice)
                else:
                    split_endpoints.append(base_endpoint)
                    base_endpoint = choice
        if base_endpoint is not None:
            split_endpoints.append(base_endpoint)
        if len(split_endpoints) > 1:
            for idx in range(len(split_endpoints) - 1):
                test = split_endpoints[idx][1] + 1
                if 0 <= test <= bounds:
                    return test * 4000000 + row


def manhatten_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def is_overlap(point1, point2):
    return point1[0] <= point2[1] and point1[1] >= point2[0]


def get_overlap(point1, point2):
    return min(point1[0], point2[0]), max(point1[1], point2[1])


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(part_1(data))
    print(part_2_2(data))


def part_2_2(data):
    # find all perimeter lines
    # and check intersection with each other and with box
    bounds = 4000000
    beacons = set()
    sensor_distances = dict()
    lines_a = defaultdict(int)
    lines_b = defaultdict(int)
    for sensor, beacon in data:
        beacons.add(beacon)
        exclusion_distance = manhatten_distance(sensor, beacon)
        sensor_distances[sensor] = exclusion_distance
        coord_x, coord_y = sensor
        coord_a, coord_b = convert_rotate((coord_x + exclusion_distance + 1, coord_y))
        lines_a[coord_a] += 1
        lines_b[coord_b] += 1
        coord_a, coord_b = convert_rotate((coord_x - exclusion_distance - 1, coord_y))
        lines_a[coord_a] += 1
        lines_b[coord_b] += 1
    # lines are a,b for both
    # if solution entirely within space, multiple lines must intersect
    mutliple_a = set(coord for coord, count in lines_a.items() if count > 1)
    mutliple_b = set(coord for coord, count in lines_b.items() if count > 1)
    for rotated_point in product(mutliple_a, mutliple_b):
        normal_point = convert_back(rotated_point)
        if 0 <= normal_point[0] <= bounds and 0 <= normal_point[1] <= bounds:
            for sensor, exclusion_distance in sensor_distances.items():
                if manhatten_distance(sensor, normal_point) <= exclusion_distance:
                    break
            else:
                return normal_point[0] * 4000000 + normal_point[1]
    # otherwise must intersect 0,4000000 box boundary
    box_points = set()
    for edge in (0, bounds):
        for coord_a in lines_a.keys():
            # x = edge
            box_points.add((edge, coord_a - edge))
            # y = edge
            box_points.add((coord_a - edge, edge))
        for coord_b in lines_b.keys():
            # x = edge
            box_points.add((edge, edge - coord_b))
            # y = edge
            box_points.add((edge + coord_b, edge))
    for point in box_points:
        if 0 <= point[0] <= bounds and 0 <= point[1] <= bounds:
            for sensor, exclusion_distance in sensor_distances.items():
                if manhatten_distance(sensor, point) <= exclusion_distance:
                    break
            else:
                return point[0] * 4000000 + point[1]


def convert_rotate(point):
    coord_x, coord_y = point
    coord_a = coord_x + coord_y
    coord_b = coord_x - coord_y
    return coord_a, coord_b


def convert_back(point):
    coord_a, coord_b = point
    coord_x = (coord_a + coord_b) // 2
    coord_y = (coord_a - coord_b) // 2
    return coord_x, coord_y

if __name__ == "__main__":
    main()
