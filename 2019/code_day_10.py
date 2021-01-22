from math import gcd


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [list(datum) for datum in data]
    return data


def place_station(data):
    rows = len(data)
    cols = len(data[0])
    asteroids = set()
    for r in range(rows):
        for c in range(cols):
            if data[r][c] == '#':
               asteroids.add((r,c))
    max_seens = 0
    for base_r, base_c in asteroids:
        seens = set()
        for r, c in asteroids:
            r_diff, c_diff = r - base_r, c - base_c
            if r_diff or c_diff:
                step = gcd(r_diff, c_diff)
                seens.add((r_diff // step, c_diff // step))
        if len(seens) > max_seens:
            max_seens = len(seens)
            location = base_r, base_c
    return max_seens, location, asteroids


def rotate(location):
    y, x = location
    if x > 0:
        return (1, -y / x)
    elif x < 0:
        return (-1, -y / x)
    # otherwise x = 0
    elif y > 0:
        return (0, 0)
    else:
        return (2, 0)


def zap_asteroids(location, asteroids, data):
    base_r, base_c = location
    seens = dict()
    for r, c in asteroids:
        r_diff, c_diff = r - base_r, c - base_c
        if r_diff or c_diff:
            step = gcd(r_diff, c_diff)
            key = (r_diff // step, c_diff // step)
            if key not in seens:
                seens[key] = (r, c)
            else:
                old_r_diff = seens[key][0] - base_r
                old_c_diff = seens[key][1] - base_r
                if old_r_diff ** 2 + old_c_diff ** 2 > r_diff ** 2 + c_diff ** 2:
                    seens[key] = (r, c)
    for _ in range(200):
        choice = max(seens, key=rotate)
        last = seens[choice]
        del seens[choice]
    return last[0] + last[1] * 100


def main():
    year, day = 2019, 10
    data = get_data(year, day)
    max_seens, location, asteroids = place_station(data)
    print(max_seens)
    print(zap_asteroids(location, asteroids, data))


if __name__ == "__main__":
    main()
