from heapdict import heapdict
from itertools import count


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [list(datum) for datum in data]
    return data


class ElfDeathError(ValueError):
    pass


class Unit:
    def __init__(self, team, r, c, elf_power):
        self.team = team
        self.hp = 200
        if team == 'G':
            self.power = 3
        else:
            self.power = elf_power
        self.loc = (r, c)
    
    def __repr__(self):
        return self.team + '(' + str(self.hp) + ')'


class Game:
    def __init__(self, board, elf_power=3):
        self.UNIT_TYPES = ('G', 'E')
        self.DIRECTIONS = ((-1, 0), (0, -1), (0, 1), (1, 0))
        self.board = board
        self.rows = len(self.board)
        self.cols = len(self.board[0])
        self.turns_completed = 0
        self.units = []
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.board[r][c]
                if cell in self.UNIT_TYPES:
                    self.units.append(Unit(cell, r, c, elf_power))
        self.g_alive = set(unit for unit in self.units if unit.team == 'G')
        self.e_alive = set(unit for unit in self.units if unit.team == 'E')

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.board])
    
    def run_game(self):
        while True:
            self.units.sort(key=lambda x: x.loc)
            exit_code = self.take_turn()
            if exit_code:
                break
        return self.score()
    
    def take_turn(self):
        for unit in self.units:
            if not self.g_alive or not self.e_alive:
                return 1
            if unit.hp > 0:
                self.move(unit)
                self.attack(unit)
        self.turns_completed += 1
        return 0

    def score(self):
        return sum(unit.hp for unit in self.units) * self.turns_completed
    
    def move(self, unit):
        # loop to find targets
        start = unit.loc
        targets = {}
        if unit.team == 'G':
            target_team = self.e_alive
        else:
            target_team = self.g_alive
        for enemy in target_team:
            r, c = enemy.loc
            for dr, dc in self.DIRECTIONS:
                a, b = pos = r + dr, c + dc
                if self.board[a][b] == '.':
                    targets[pos] = (float('inf'), a, b, -1)
                elif pos == start:
                    return
        # above stops if unit next to a target
        # stop if no targets
        r, c = start = unit.loc
        if not targets:
            return
        # initialise loop
        distances = heapdict()
        for dir_idx, direction in enumerate(self.DIRECTIONS):
            dr, dc = direction
            a, b = pos = r + dr, c + dc
            if self.board[a][b] == '.':
                distances[pos] = (1, dir_idx)
        seens = set()
        # perform loop
        while distances:
            choice, details = distances.popitem()
            r, c = choice
            distance, dir_idx = details
            if choice in targets:
                targets[choice] = (distance, r, c, dir_idx)
            seens.add(choice)
            for dr, dc in self.DIRECTIONS:
                a, b = pos = r + dr, c + dc
                if pos not in seens:
                    if self.board[a][b] == '.':
                        if pos in distances:
                            if distances[pos] > (distance + 1, dir_idx):
                                distances[pos] = (distance + 1, dir_idx)
                        else:
                            distances[pos] = (distance + 1, dir_idx)
        # do movement
        final_direction = targets[min(targets, key=targets.get)][-1]
        if final_direction == -1:
            return
        r, c = unit.loc
        dr, dc = self.DIRECTIONS[final_direction]
        self.board[r][c] = '.'
        self.board[r + dr][c + dc] = unit.team
        unit.loc = (r + dr, c + dc)

    def attack(self, unit):
        r, c = unit.loc
        targets = set()
        neighbours = set((r+dr, c+dc) for dr, dc in self.DIRECTIONS)
        if unit.team == 'G':
            target_team = self.e_alive
        else:
            target_team = self.g_alive
        for potential_target in target_team:
            if potential_target.loc in neighbours:
                targets.add(potential_target)
        if targets:
            target = min(targets, key=lambda x: (x.hp, x.loc))
            target.hp -= unit.power
            if target.hp <= 0:
                target.hp = 0
                a, b = target.loc
                if unit.team == 'G':
                    self.e_alive.remove(target)
                else:
                    self.g_alive.remove(target)
                self.board[a][b] = '.'
                target.loc = (-1, -1)


class NoElfDeaths:
    def __init__(self, board, elf_power=3):
        self.UNIT_TYPES = ('G', 'E')
        self.DIRECTIONS = ((-1, 0), (0, -1), (0, 1), (1, 0))
        self.board = board
        self.rows = len(self.board)
        self.cols = len(self.board[0])
        self.turns_completed = 0
        self.units = []
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.board[r][c]
                if cell in self.UNIT_TYPES:
                    self.units.append(Unit(cell, r, c, elf_power))
        self.g_alive = set(unit for unit in self.units if unit.team == 'G')
        self.e_alive = set(unit for unit in self.units if unit.team == 'E')

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.board])
    
    def run_game(self):
        while True:
            self.units.sort(key=lambda x: x.loc)
            exit_code = self.take_turn()
            if exit_code:
                break
        return self.score()
    
    def take_turn(self):
        for unit in self.units:
            if not self.g_alive or not self.e_alive:
                return 1
            if unit.hp > 0:
                self.move(unit)
                self.attack(unit)
        self.turns_completed += 1
        return 0

    def score(self):
        return sum(unit.hp for unit in self.units) * self.turns_completed
    
    def move(self, unit):
        # loop to find targets
        start = unit.loc
        targets = {}
        if unit.team == 'G':
            target_team = self.e_alive
        else:
            target_team = self.g_alive
        for enemy in target_team:
            r, c = enemy.loc
            for dr, dc in self.DIRECTIONS:
                a, b = pos = r + dr, c + dc
                if self.board[a][b] == '.':
                    targets[pos] = (float('inf'), a, b, -1)
                elif pos == start:
                    return
        # above stops if unit next to a target
        # stop if no targets
        r, c = start = unit.loc
        if not targets:
            return
        # initialise loop
        distances = heapdict()
        for dir_idx, direction in enumerate(self.DIRECTIONS):
            dr, dc = direction
            a, b = pos = r + dr, c + dc
            if self.board[a][b] == '.':
                distances[pos] = (1, dir_idx)
        seens = set()
        # perform loop
        while distances:
            choice, details = distances.popitem()
            r, c = choice
            distance, dir_idx = details
            if choice in targets:
                targets[choice] = (distance, r, c, dir_idx)
            seens.add(choice)
            for dr, dc in self.DIRECTIONS:
                a, b = pos = r + dr, c + dc
                if pos not in seens:
                    if self.board[a][b] == '.':
                        if pos in distances:
                            if distances[pos] > (distance + 1, dir_idx):
                                distances[pos] = (distance + 1, dir_idx)
                        else:
                            distances[pos] = (distance + 1, dir_idx)
        # do movement
        final_direction = targets[min(targets, key=targets.get)][-1]
        if final_direction == -1:
            return
        r, c = unit.loc
        dr, dc = self.DIRECTIONS[final_direction]
        self.board[r][c] = '.'
        self.board[r + dr][c + dc] = unit.team
        unit.loc = (r + dr, c + dc)

    def attack(self, unit):
        r, c = unit.loc
        targets = set()
        neighbours = set((r+dr, c+dc) for dr, dc in self.DIRECTIONS)
        if unit.team == 'G':
            target_team = self.e_alive
        else:
            target_team = self.g_alive
        for potential_target in target_team:
            if potential_target.loc in neighbours:
                targets.add(potential_target)
        if targets:
            target = min(targets, key=lambda x: (x.hp, x.loc))
            target.hp -= unit.power
            if target.hp <= 0:
                target.hp = 0
                a, b = target.loc
                if unit.team == 'G':
                    self.e_alive.remove(target)
                    raise ElfDeathError
                else:
                    self.g_alive.remove(target)
                self.board[a][b] = '.'
                target.loc = (-1, -1)


def outnumbered(data):
    data = [row.copy() for row in data]
    game = Game(data)
    return game.run_game()


def overpower(data):
    for n in count(4):
        new_data = [row.copy() for row in data]
        no_deaths_game = NoElfDeaths(new_data, n)
        try:
            return no_deaths_game.run_game()
        except ElfDeathError:
            continue


def main():
    year, day = 2018, 15
    data = get_data(year, day)
    print(outnumbered(data))
    print(overpower(data))


if __name__ == "__main__":
    main()
