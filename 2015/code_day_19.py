def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    starter = data[1]
    data = [preprocess(datum) for datum in data[0].splitlines()]
    return data, starter


def preprocess(datum):
    datum = datum.split()
    return datum[0], datum[2]


def count_variations(data, starter):
    ways = set()
    for find, replace in data:
        min_index = 0
        for _ in range(starter.count(find)):
            idx = starter.index(find, min_index)
            min_index = idx + 1
            ways.add(starter[:idx] + starter[idx:].replace(find, replace, 1))
    return len(ways)


def context_free_trick(data, starter):
    # can do this because we have 4 types of modification
    #   1.  A => B C
    #   2.  A => B Rn C Ar
    #   3.  A => B Rn C Y D Ar
    #   4.  A => B Rn C Y D Y E Ar
    # Thus we can form a series of equations, and solve to get the following.
    num_elements = sum(65 <= ord(character) <91 for character in starter)
    Rn = starter.count('Rn')
    Y = starter.count('Y')
    return num_elements - 2*Rn - 2*Y - 1


def main():
    year, day = 2015, 19
    data, starter = get_data(year, day)
    print(count_variations(data, starter))
    print(context_free_trick(data, starter))


if __name__ == "__main__":
    main()
