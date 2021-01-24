def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum


def group_score(data):
    idx = 0
    n = len(data)
    garbage = False
    score = 0
    value = 0
    while idx < n:
        if data[idx] == '!':
            idx += 2
            continue
        else:
            if garbage:
                if data[idx] == '>':
                    garbage = False
            else:
                if data[idx] == '<':
                    garbage = True
                elif data[idx] == '{':
                    value += 1
                elif data[idx] == '}':
                    score += value
                    value -= 1
            idx += 1
    return score


def garbage_count(data):
    idx = 0
    n = len(data)
    garbage = False
    score = 0
    while idx < n:
        if data[idx] == '!':
            idx += 2
            continue
        else:
            if garbage:
                if data[idx] == '>':
                    garbage = False
                else:
                    score += 1
            else:
                if data[idx] == '<':
                    garbage = True
                elif data[idx] == '{':
                    pass
                elif data[idx] == '}':
                    pass
            idx += 1
    return score


def main():
    year, day = 2017, 9
    data = get_data(year, day)
    print(group_score(data))
    print(garbage_count(data))


if __name__ == "__main__":
    main()
