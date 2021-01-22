def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum


def reduce_list(data):
    new_list = []
    for element in data:
        new_item = ord(element)
        if not new_list:
            new_list.append(new_item)
        else:
            if abs(new_list[-1] - new_item) == 32:
                new_list.pop()
            else:
                new_list.append(new_item)
    return new_list


def react(data):
    data = reduce_list(data)
    return len(data)


def reduce_ignoring(data, ignore):
    new_list = []
    for new_item in data:
        if new_item == ignore or new_item == ignore + 32:
            continue
        else:
            if not new_list:
                new_list.append(new_item)
            else:
                if abs(new_list[-1] - new_item) == 32:
                    new_list.pop()
                else:
                    new_list.append(new_item)
    return new_list


def react_improvement(data):
    data = reduce_list(data)
    min_len = len(data)
    for ignore in range(65, 91):
        attempt_len = len(reduce_ignoring(data, ignore))
        min_len = min(attempt_len, min_len)
    return min_len


def main():
    year, day = 2018, 5
    data = get_data(year, day)
    print(react(data))
    print(react_improvement(data))


if __name__ == "__main__":
    main()
