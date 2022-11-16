def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    instruction, region = datum.split()
    instruction = 1 if instruction == 'on' else 0
    region = region.split(',')
    region = tuple(tuple(int(val) for val in coord[2:].split('..')) for coord in region)
    return instruction, region


def initialize_reactor(data):
    new_rows = []
    for row in data:
        if abs(row[1][0][0]) <= 50:
            new_rows.append(row)
    return reboot_reactor(new_rows)


def reboot_reactor(data):
    volume = 0
    placed = set()
    # go through rows in reverse
    for row in reversed(list(data)):
        instruction, region = row
        # if instuction is off, don't need to do anything
        if instruction:
            overlaps = set()
            for placed_row in placed:
                new_overlap = compute_overlap(region, placed_row[1])
                if new_overlap is not None:
                    overlaps.add((1, new_overlap))
            # account for double (and higher order) counting by rerunning on overlaps
            volume += compute_volume(region) - reboot_reactor(overlaps)
        placed.add((1, region))
    return volume


def compute_volume(region):
    volume = 1
    for coord in region:
        volume *= coord[1] - coord[0] + 1
    return volume


def compute_overlap(r1, r2):
    overlap = tuple((max(r1[idx][0], r2[idx][0]), min(r1[idx][1], r2[idx][1])) for idx in range(3))
    for pair in overlap:
        if pair[1] < pair[0]:
            return None
    return overlap


def main():
    year, day = 2021, 22
    data = get_data(year, day)
    print(initialize_reactor(data))
    print(reboot_reactor(data))


if __name__ == "__main__":
    main()
