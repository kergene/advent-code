def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = dict(preprocess(datum) for datum in data)
    return data


def preprocess(datum):
    datum = datum.split(')')
    return datum[1], datum[0]


class Memoize:
    def __init__(self, func):
        self.func = func
        self.memo = {}
    
    def __call__(self, value, data):
        if value not in self.memo:
            self.memo[value] = self.func(value, data)
        return self.memo[value]


@Memoize
def count_orbits(planet, data):
    if planet == 'COM':
        return 0
    else:
        return count_orbits(data[planet], data) + 1


def total_orbits(data):
    tot = 0
    for planet in data:
        tot += count_orbits(planet, data)
    return tot


def orbital_transfers(data):
    san = {}
    you = {}
    transfers = 0
    planet = data['SAN']
    san[planet] = transfers
    while planet != 'COM':
        transfers += 1
        planet = data[planet]
        san[planet] = transfers
    transfers = 0
    planet = data['YOU']
    you[planet] = transfers
    while planet != 'COM':
        transfers += 1
        planet = data[planet]
        you[planet] = transfers
    intersection = set(san).intersection(you)
    return min(you[planet] + san[planet] for planet in intersection)


def main():
    year, day = 2019, 6
    data = get_data(year, day)
    print(total_orbits(data))
    print(orbital_transfers(data))


if __name__ == "__main__":
    main()
