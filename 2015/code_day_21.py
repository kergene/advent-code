from math import ceil
from itertools import product
from itertools import combinations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    enemy = dict(preprocess_enemy(i) for i in data[0:3])
    weapons = list(preprocess_shop(i) for i in data[5:10])
    armors = list(preprocess_shop(i) for i in data[12:17])
    rings = list(preprocess_shop_rings(i) for i in data[19:25])
    # allow for no armor/rings to be selected
    armors.append({'Cost':0, 'Damage':0,  'Armor':0})
    rings.append({'Cost':0, 'Damage':0,  'Armor':0})
    rings.append({'Cost':0, 'Damage':0,  'Armor':0})
    return enemy, weapons, armors, rings


def preprocess_enemy(datum):
    datum = datum.split(':')
    return datum[0], int(datum[1].strip())


def preprocess_shop(datum):
    # shop items given separately to the input
    # faster to parse than to type
    datum = datum.split()
    return {'Cost':int(datum[1]), 'Damage':int(datum[2]), 'Armor':int(datum[3])}


def preprocess_shop_rings(datum):
    # rings contain a +n column
    datum = datum.split()
    return {'Cost':int(datum[2]), 'Damage':int(datum[3]), 'Armor':int(datum[4])}


def win(enemy, weapons, armors, rings):
    min_cost = sum(i['Cost'] for i in weapons) + sum(i['Cost'] for i in armors) + sum(i['Cost'] for i in rings)
    for sword, shield in product(weapons, armors):
        for ring1, ring2 in combinations(rings, 2):
            items = [sword, shield, ring1, ring2]
            cost = sum(i['Cost'] for i in items)
            damage = sum(i['Damage'] for i in items)
            armor = sum(i['Armor'] for i in items)
            if cost >= min_cost:
                continue
            else:
                attack_attempts = ceil(100 / max(enemy['Damage'] - armor, 1))
                damage_dealt = max(damage - enemy['Armor'], 1) * attack_attempts
                if damage_dealt >= enemy['Hit Points']:
                    min_cost = cost
    return min_cost


def lose(enemy, weapons, armors, rings):
    max_cost = 0
    for sword, shield in product(weapons, armors):
        for ring1, ring2 in combinations(rings, 2):
            items = [sword, shield, ring1, ring2]
            cost = sum(i['Cost'] for i in items)
            damage = sum(i['Damage'] for i in items)
            armor = sum(i['Armor'] for i in items)
            if cost <= max_cost:
                continue
            else:
                attack_attempts = ceil(100 / max(enemy['Damage'] - armor, 1))
                damage_dealt = max(damage - enemy['Armor'], 1) * attack_attempts
                if damage_dealt < enemy['Hit Points']:
                    max_cost = cost
    return max_cost


def main():
    year, day = 2015, 21
    enemy, weapons, armors, rings = get_data(year, day)
    print(win(enemy, weapons, armors, rings))
    print(lose(enemy, weapons, armors, rings))


if __name__ == "__main__":
    main()
