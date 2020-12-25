from itertools import product


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def value_bitmask(data):
    memory = dict()
    for line in data:
        line = line.split()
        if line[0] == 'mask':
            mask = line[2]
        else:
            value = int(line[2])
            value = list(format(value, '036b'))
            for i in range(len(mask)):
                if mask[i] == '1':
                    value[i] = '1'
                elif mask[i] == '0':
                    value[i] = '0'
            value = ''.join(value)
            location = line[0][4:-1]
            memory[location] = int(value, 2)
    return sum(memory.values())


def location_bitmask(data):
    memory = dict()
    BINARY = ('0','1')
    for line in data:
        line = line.split()
        if line[0] == 'mask':
            mask = line[2]
        else:
            value = int(line[2])
            location = int(line[0][4:-1])
            location = list(format(location, '036b'))
            floating_indices = []
            for i in range(len(mask)):
                if mask[i] == '1':
                    location[i] = '1'
                elif mask[i] == 'X':
                    floating_indices.append(i)
            for choice in product(BINARY, repeat=len(floating_indices)):
                floating_location = location.copy()
                for idx, val in enumerate(floating_indices):
                    floating_location[val] = choice[idx]
                floating_location = ''.join(floating_location)
                memory[int(floating_location, 2)] = value
    return sum(memory.values())


def main():
    year, day = 2020, 14
    data = get_data(year, day)
    print(value_bitmask(data))
    print(location_bitmask(data))


if __name__ == "__main__":
    main()
