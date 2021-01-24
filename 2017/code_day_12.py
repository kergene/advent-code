def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = dict(preprocess(datum) for datum in data)
    return data


def preprocess(datum):
    datum = datum.split(' <-> ')
    from_val = int(datum[0])
    to_vals = set(int(val) for val in datum[1].split(', '))
    return from_val, to_vals


def component_size(data):
    q = set()
    q.add(0)
    seens = set()
    while q:
        choice = q.pop()
        seens.add(choice)
        for to_val in data[choice]:
            if to_val not in seens:
                q.add(to_val)
    return len(seens)


def component_count(data):
    all_nodes = set(data.keys())
    group_count = 0
    while all_nodes:
        group_count += 1
        group_choice = all_nodes.pop()
        q = set()
        q.add(group_choice)
        seens = set()
        while q:
            choice = q.pop()
            seens.add(choice)
            for to_val in data[choice]:
                if to_val not in seens:
                    if to_val not in q:
                        q.add(to_val)
                        all_nodes.remove(to_val)
    return group_count


def main():
    year, day = 2017, 12
    data = get_data(year, day)
    print(component_size(data))
    print(component_count(data))


if __name__ == "__main__":
    main()
