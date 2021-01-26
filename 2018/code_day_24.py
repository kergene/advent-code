def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    return data


def make_troops(team):
    team = team.splitlines()
    army = set()
    side = team[0][:-1]
    for line in team[1:]:
        line = line.replace('(', '')
        line = line.split()
        units = int(line[0])
        damage = int(line[-6])
        hp = int(line[4])
        initiative = int(line[-1])
        attack_type = line[-5]
        weaknesses = []
        if 'weak' in line:
            idx = line.index('weak') + 2
            weaknesses.append(line[idx])
            while weaknesses[-1][-1] not in (';)'):
                weaknesses[-1] = weaknesses[-1][:-1]
                idx += 1
                weaknesses.append(line[idx])
            weaknesses[-1] = weaknesses[-1][:-1]
        immunities = []
        if 'immune' in line:
            idx = line.index('immune') + 2
            immunities.append(line[idx])
            while immunities[-1][-1] not in (';)'):
                immunities[-1] = immunities[-1][:-1]
                idx += 1
                immunities.append(line[idx])
            immunities[-1] = immunities[-1][:-1]
        army.add(Group(units, damage, hp, initiative, attack_type, weaknesses, immunities, side))
    return army


class Group:
    def __init__(self, units, damage, hp, initiative, attack_type, weaknesses, immunities, team):
        self.units = units
        self.damage = damage
        self.hp = hp
        self.initiative = initiative
        self.attack_type = attack_type
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.team = team
    
    def __repr__(self):
        state = [
            'Group:',
            self.team,
            self.units,
            self.damage,
            self.hp,
            self.initiative,
            self.attack_type,
            self.weaknesses,
            self.immunities
        ]
        return '\n\t'.join(str(item) for item in state)
    
    def __hash__(self):
        return self.initiative
    
    @property
    def effective_power(self):
        return self.units * self.damage
    
    def reset(self):
        self.being_attacked = False
        self.weak = False
        self.target = None


class Battle:
    def __init__(self, teams, boost):
        self.immune_system = teams[0]
        self.infection = teams[1]
        self.players = self.immune_system | self.infection
        self.boost(boost)
    
    def boost(self, boost):
        for unit in self.immune_system:
            unit.damage += boost
    
    def fight(self):
        self.killed_total = 1
        while self.immune_system and self.infection and self.killed_total:
            self.play_round()
        if self.killed_total > 0:
            return self.units_remaining(), 1 if self.immune_system else 0
        else:
            return self.units_remaining(), 2

    def play_round(self):
        self.reset_units()
        self.target_selection()
        self.attacking()

    def reset_units(self):
        for unit in self.players:
            unit.reset()

    def target_selection(self):
        for attacker in sorted(self.players, key=lambda team: (team.effective_power, team.initiative), reverse=True):
            attack_type = attacker.attack_type
            if attacker.team == 'Immune System':
                targets = self.infection
            elif attacker.team == 'Infection':
                targets = self.immune_system
            else:
                assert False, attacker.team
            targets = [group for group in targets if (not group.being_attacked) and (attack_type not in group.immunities)]
            weakest = [group for group in targets if attack_type in group.weaknesses]
            if weakest:
                selected = max(weakest, key=lambda team: (team.effective_power, team.initiative))
                selected.weak = True
                selected.being_attacked = True
                attacker.target = selected
            elif targets:
                selected = max(targets, key=lambda team: (team.effective_power, team.initiative))
                selected.being_attacked = True
                attacker.target = selected
            else:
                continue

    def attacking(self):
        self.killed_total = 0
        for attacker in sorted(self.players, key=lambda team: team.initiative, reverse=True):
            if attacker.target is not None:
                defender = attacker.target
                damage = attacker.effective_power
                if defender.weak:
                    damage *= 2
                killed = damage // defender.hp
                self.killed_total += killed
                defender.units -= killed
                if defender.units <= 0:
                    defender.units = 0
                    self.players.remove(defender)
                    if defender.team == 'Immune System':
                        self.immune_system.remove(defender)
                    elif defender.team == 'Infection':
                        self.infection.remove(defender)
                    else:
                        assert False, defender.team
    
    def units_remaining(self):
        return sum(group.units for group in self.players)


def run_fight(data):
    teams = [make_troops(datum) for datum in data]
    battle = Battle(teams, 0)
    return battle.fight()[0]


def boost_reindeer(data):
    boost = 0
    while True:
        teams = [make_troops(datum) for datum in data]
        battle = Battle(teams, boost)
        troops, winner = battle.fight()
        if winner == 1:
            return troops
        else:
            boost += 1


def main():
    year, day = 2018, 24
    data = get_data(year, day)
    print(run_fight(data))
    print(boost_reindeer(data))


if __name__ == "__main__":
    main()
