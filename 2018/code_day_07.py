from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    dependencies = defaultdict(set)
    for first, last in data:
        dependencies[last].add(first)
    return dependencies


def preprocess(datum):
    datum = datum.split()
    return datum[1], datum[-3]


def build_ordering(dependencies):
    ordering = []
    not_fixed = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    fixed = set()
    while not_fixed:
        for letter in not_fixed:
            if all(completed in fixed for completed in dependencies[letter]):
                ordering.append(letter)
                not_fixed.remove(letter)
                fixed.add(letter)
                break
    return ''.join(ordering)


def second_smallest(numbers):
    min_1 = min_2 = max(numbers)
    for test in numbers:
        if test <= min_1:
            min_1, min_2 = test, min_1
        elif test < min_2:
            min_2 = test
    return min_2


def multi_worker_time(dependencies):
    not_started = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    n_workers = 5
    done = set()
    time = -1
    finish_times = [0] * n_workers
    doing = [-1] * n_workers
    while len(done) != 26:
        time += 1
        for worker in range(n_workers):
            if finish_times[worker] == time:
                if doing[worker] != -1:
                    done.add(doing[worker])
                    doing[worker] = -1
        for worker in range(n_workers):
            if finish_times[worker] == time:
                for letter in not_started:
                    if all(completed in done for completed in dependencies[letter]):
                        finish_times[worker] += ord(letter) - 5
                        doing[worker] = letter
                        not_started.remove(letter)
                        break
                finish_times[worker] += 1
    return time


def main():
    year, day = 2018, 7
    data = get_data(year, day)
    print(build_ordering(data))
    print(multi_worker_time(data))


if __name__ == "__main__":
    main()
