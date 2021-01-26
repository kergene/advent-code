from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    data = (
        data.replace('<', '(')
            .replace('>', ')')
            .replace('=', ':')
            .replace('\n', '}, {')
            .replace('p', "'p'")
            .replace('v', "'v'")
            .replace('a', "'a'")
    )
    data = ''.join(['{', data, '}'])
    data = eval(data)
    return data


class Particle:
    def __init__(self, vals, idx):
        self.idx = idx
        self.pos = list(vals['p'])
        self.vel = list(vals['v'])
        self.acc = list(vals['a'])
    
    def update(self):
        for idx in range(3):
            self.vel[idx] += self.acc[idx]
            self.pos[idx] += self.vel[idx]
    
    def __repr__(self):
        string = [
            'Particle:',
            self.pos,
            self.vel,
            self.acc
        ]
        return '\n\t'.join(str(val) for val in string)
    
    def increasing(self):
        for idx in range(2):
            if self.vel[idx] * self.acc[idx] < 0:
                return False
        return True
    
    def __hash__(self):
        return self.idx


def closest_particle(data):
    # long term is min acceleration
    # ties broken by min velocity (once signs all match)
    # no more ties in this case
    n = len(data)
    min_acc = min(manhattan_zero(data[idx]['a']) for idx in range(n))
    possibles = [idx for idx in range(n) if manhattan_zero(data[idx]['a']) == min_acc]
    if len(possibles) == 1:
        return possibles[0]
    else:
        particles = [Particle(data[idx], idx) for idx in possibles]
        while not all(particle.increasing() for particle in particles):
            for particle in particles:
                particle.update()
        min_vel = min(manhattan_zero(particle.vel) for particle in particles)
        particles = [particle for particle in particles if manhattan_zero(particle.vel) == min_vel]
        if len(particles) == 1:
            return particles[0].idx
        else:
            assert False, 'More needed'


def manhattan_distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def manhattan_zero(a):
    ORIGIN = (0, 0, 0)
    return manhattan_distance(a, ORIGIN)


def collision_removal(data):
    # we stop when no change in number of particles for 50 steps
    # (not guaranteed to reach solution, but works for input)
    n = len(data)
    particles = [Particle(data[idx], idx) for idx in range(n)]
    lengths = [n]
    for _ in range(50):
        for particle in particles:
            particle.update()
        particles = pos_check(particles)
        lengths.append(len(particles))
    while True:
        for particle in particles:
            particle.update()
        particles = pos_check(particles)
        if lengths[-50] == len(particles):
            return len(particles)
        else:
            lengths.append(len(particles))


def pos_check(particles):
    positions = defaultdict(list)
    for particle in particles:
        positions[tuple(particle.pos)].append(particle)
    survived_particles = []
    for state in positions.values():
        if len(state) == 1:
            survived_particles.append(state[0])
    return survived_particles


def main():
    year, day = 2017, 20
    data = get_data(year, day)
    print(closest_particle(data))
    print(collision_removal(data))


if __name__ == "__main__":
    main()
