from itertools import combinations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [int(i) for i in data]
    return data


def find_invalid(data):
    for i in range(25,len(data)):
        test = data[i]
        pre_set = data[i-25:i]
        flag = False
        for i, j in combinations(pre_set, 2):
            if i + j == test:
                flag = True
                break
        if not flag:
            return test


def find_continuous_sum(data, target):
    min_idx = 0
    max_idx = 1
    total = data[0] + data[1]
    while True:
        if total == target:
            # return min * max
            subdata = data[min_idx:max_idx + 1]
            return min(subdata) + max(subdata)
        elif total < target or max_idx - min_idx == 1:
            # add next element
            max_idx += 1
            total += data[max_idx]
        else:
            # remove first element
            total -= data[min_idx]
            min_idx += 1


def main():
    year, day = 2020, 9
    data = get_data(year, day)
    invalid = find_invalid(data)
    print(invalid)
    print(find_continuous_sum(data, invalid))


if __name__ == "__main__":
    main()
