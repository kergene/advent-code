from itertools import product


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


class Lights:
    def __init__(self):
        self.lights = [[0 for _ in range(1000)] for _ in range(1000)]

    def switch_lights(self, rule):
        rule = rule.split()
        max_cell = rule[-1].split(',')
        max_cell = tuple(int(i) for i in max_cell)
        min_cell = rule[-3].split(',')
        min_cell = tuple(int(i) for i in min_cell)
        switch_range = product(range(min_cell[0], max_cell[0] + 1), range(min_cell[1], max_cell[1] + 1))
        if rule[-4] == 'on':
            for i, j in switch_range:
                self.lights[i][j] = 1
        elif rule[-4] == 'off':
            for i, j in switch_range:
                self.lights[i][j] = 0
        elif rule[-4] == 'toggle':
            for i, j in switch_range:
                self.lights[i][j] = 1 - self.lights[i][j]
        else:
            raise ValueError()

    def super_switch_lights(self, rule):
        rule = rule.split()
        max_cell = rule[-1].split(',')
        max_cell = tuple(int(i) for i in max_cell)
        min_cell = rule[-3].split(',')
        min_cell = tuple(int(i) for i in min_cell)
        switch_range = product(range(min_cell[0], max_cell[0] + 1), range(min_cell[1], max_cell[1] + 1))
        if rule[-4] == 'on':
            for i, j in switch_range:
                self.lights[i][j] += 1
        elif rule[-4] == 'off':
            for i, j in switch_range:
                self.lights[i][j] = max(0, self.lights[i][j] - 1)
        elif rule[-4] == 'toggle':
            for i, j in switch_range:
                self.lights[i][j] += 2
        else:
            raise ValueError()

    def party_mode(self, rules):
        self.reset()
        for rule in rules:
            self.switch_lights(rule)
        return self.count_on()

    def super_party_mode(self, rules):
        self.reset()
        for rule in rules:
            self.super_switch_lights(rule)
        return self.count_on()

    def count_on(self):
        return sum(sum(row) for row in self.lights)

    def reset(self):
        self.lights = [[0 for _ in range(1000)] for _ in range(1000)]


def main():
    year, day = 2015, 6
    rules = get_data(year, day)
    lights = Lights()
    print(lights.party_mode(rules))
    print(lights.super_party_mode(rules))


if __name__ == "__main__":
    main()
