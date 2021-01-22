from numpy import lcm
from itertools import combinations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = datum[1:-1].split(',')
    return [int(coord.split('=')[1]) for coord in datum]


class Moon:
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def __str__(self):
        return (f'x = {self.x}, y = {self.x}, z = {self.z}' + '\n' +
            f'vx = {self.vx}, vy = {self.vx}, vz = {self.vz}')

    def adjust_velocity(self, other):
        self.vx += (self.x < other.x)
        self.vx -= (self.x > other.x)
        self.vy += (self.y < other.y)
        self.vy -= (self.y > other.y)
        self.vz += (self.z < other.z)
        self.vz -= (self.z > other.z)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    @property
    def total_energy(self):
        return self.kinetic_energy * self.potential_energy

    @property
    def kinetic_energy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    @property
    def potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


class SolarSystem:
    def __init__(self, positions):
        self.moons = [Moon(pos) for pos in positions]
    
    def apply_gravity(self):
        for moon_a, moon_b in combinations(self.moons, r=2):
            moon_a.adjust_velocity(moon_b)
            moon_b.adjust_velocity(moon_a)

    def apply_velocity(self):
        for moon in self.moons:
            moon.move()
    
    def total_energy(self):
        return sum(moon.total_energy for moon in self.moons)


def system_energy(positions):
    jupiter = SolarSystem(positions)
    for _ in range(1000):
        jupiter.apply_gravity()
        jupiter.apply_velocity()
    return jupiter.total_energy()


class Moon1D:
    def __init__(self, position, index):
        self.x = position[index]
        self.vx = 0

    def adjust_velocity(self, other):
        self.vx += (self.x < other.x)
        self.vx -= (self.x > other.x)

    def move(self):
        self.x += self.vx


class SolarSystem1D:
    def __init__(self, positions, index):
        self.moons = [Moon1D(pos, index) for pos in positions]
    
    def apply_gravity(self):
        for moon_a, moon_b in combinations(self.moons, r=2):
            moon_a.adjust_velocity(moon_b)
            moon_b.adjust_velocity(moon_a)

    def apply_velocity(self):
        for moon in self.moons:
            moon.move()
    
    def get_states(self):
        state = []
        for moon in self.moons:
            state.append(moon.x)
            state.append(moon.vx)
        return tuple(state)


def loop_finder(positions):
    return_times = []
    for dimension in range(3):
        jupiter = SolarSystem1D(positions, dimension)
        steps = 0
        states = dict()
        states[jupiter.get_states()] = steps
        while True:
            steps += 1
            jupiter.apply_gravity()
            jupiter.apply_velocity()
            new_state = jupiter.get_states()
            if new_state in states:
                out = steps - states[new_state]
                break
            else:
                states[new_state] = steps
        return_times.append(out)
    return lcm.reduce(return_times)


def main():
    year, day = 2019, 12
    data = get_data(year, day)
    print(system_energy(data))
    print(loop_finder(data))


if __name__ == "__main__":
    main()
