def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = datum.split('-')
    return int(datum[0]), int(datum[1])


def least_unblocked(data):
    ip_test = 0
    data = sorted(data, key=lambda x: x[0])
    while True:
        next_potentially_free = [pair[1] for pair in data if ip_test >= pair[0] and pair[1] >= ip_test]
        if len(next_potentially_free) == 0:
            return ip_test
        else:
            ip_test = max(next_potentially_free) + 1


def total_unblocked(data):
    max_ip = 4294967295
    allowed_count = 0
    ip_test = 0
    data = sorted(data, key=lambda x: x[0])
    while True:
        if ip_test > max_ip:
            return allowed_count
        next_potentially_free = [pair[1] for pair in data if ip_test >= pair[0] and pair[1] >= ip_test]
        if len(next_potentially_free) == 0:
            future_blocked = [pair[0] for pair in data if pair[0] > ip_test]
            if len(future_blocked) == 0:
                # deals with end being unblocked
                allowed_count += max_ip - ip_test + 1
                return allowed_count
            else:
                next_blocked = min(future_blocked)
                allowed_count += next_blocked - ip_test
                ip_test = next_blocked
        else:
            ip_test = max(next_potentially_free) + 1


def main():
    year, day = 2016, 20
    data = get_data(year, day)
    print(least_unblocked(data))
    print(total_unblocked(data))


if __name__ == "__main__":
    main()
