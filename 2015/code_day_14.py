def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = datum.split()
    return int(datum[3]), int(datum[6]), int(datum[13])


def race(data):
    total_time = 2503
    max_dist = 0
    for speed, time, break_time in data:
        tot_time = time + break_time
        base_dist = speed * time * (total_time // tot_time)
        remaining_time = total_time % tot_time
        base_dist += min(remaining_time, time) * speed
        if base_dist > max_dist:
            max_dist = base_dist
    return max_dist


def points_race(data):
    total_time = 2503
    points = dict((i, [0, 0, 0, -1]) for i in data) # list is: no. of points, distance so far, time since last break, time since last run (should have used dict for this)
    for _ in range(total_time):
        for reindeer in data:
            if points[reindeer][2] != -1:
                points[reindeer][1] += reindeer[0]
                points[reindeer][2] += 1
                if points[reindeer][2] == reindeer[1]:
                    points[reindeer][2] = -1
                    points[reindeer][3] = 0
            else:
                points[reindeer][3] += 1
                if points[reindeer][3] == reindeer[2]:
                    points[reindeer][3] = -1
                    points[reindeer][2] = 0
        max_dist = max(i[1] for i in points.values())
        for reindeer in data:
            if points[reindeer][1] == max_dist:
                points[reindeer][0] += 1
    return max(i[0] for i in points.values())


def main():
    year, day = 2015, 14
    data = get_data(year, day)
    print(race(data))
    print(points_race(data))


if __name__ == "__main__":
    main()
