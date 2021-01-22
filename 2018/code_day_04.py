from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = dict(preprocess(datum) for datum in data)
    return data


def preprocess(datum):
    date = datum[1:17]
    return date, datum[19:]


def guard_strat_1(data):
    # will do with two passes
    guard_time = defaultdict(int)
    sorted_keys = sorted(data)
    for timestamp in sorted_keys:
        action = data[timestamp].split()
        if action[0] == 'Guard':
            guard = int(action[1][1:])
        elif action[0] == 'falls':
            sleep_time = int(timestamp.split(':')[1])
        elif action[0] == 'wakes':
            wake_time = int(timestamp.split(':')[1])
            guard_time[guard] += wake_time - sleep_time
        else:
            assert False, action
    sleepy_guard = max(guard_time, key=guard_time.get)
    sleep_times = defaultdict(int)
    for timestamp in sorted_keys:
        action = data[timestamp].split()
        if action[0] == 'Guard':
            guard = int(action[1][1:])
        elif action[0] == 'falls':
            sleep_time = int(timestamp.split(':')[1])
        elif action[0] == 'wakes':
            wake_time = int(timestamp.split(':')[1])
            if guard == sleepy_guard:
                for minute in range(sleep_time, wake_time):
                    sleep_times[minute] += 1
        else:
            assert False, action
    sleepy_minute = max(sleep_times, key=sleep_times.get)
    return sleepy_guard * sleepy_minute


def guard_strat_2(data):
    sorted_keys = sorted(data)
    guard_sleep_times = defaultdict(int)
    for timestamp in sorted_keys:
        action = data[timestamp].split()
        if action[0] == 'Guard':
            guard = int(action[1][1:])
        elif action[0] == 'falls':
            sleep_time = int(timestamp.split(':')[1])
        elif action[0] == 'wakes':
            wake_time = int(timestamp.split(':')[1])
            for minute in range(sleep_time, wake_time):
                guard_sleep_times[guard, minute] += 1
        else:
            assert False, action
    sleepy_guard, sleepy_minute = max(guard_sleep_times, key=guard_sleep_times.get)
    return sleepy_guard * sleepy_minute


def main():
    year, day = 2018, 4
    data = get_data(year, day)
    print(guard_strat_1(data))
    print(guard_strat_2(data))


if __name__ == "__main__":
    main()
