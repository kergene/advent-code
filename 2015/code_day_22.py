def get_data(year, day): # this is not nice code
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = dict(preprocess(datum) for datum in data)
    spells = {'mm': [4, 0, 0,   0,  53, 1], # [damage, heal, armor, mana, cost, effect_length]
              'dr': [2, 2, 0,   0,  73, 1], # largely hard coded rather than used
              'sh': [0, 0, 7,   0, 113, 6],
              'po': [3, 0, 0,   0, 173, 6],
              're': [0, 0, 0, 101, 229, 5]
    }
    return data, spells


def preprocess(datum):
    datum = datum.split(':')
    return datum[0], int(datum[1])


def calculate_state(hist, boss, spells):
    mana = 500
    hp = 50
    boss_hp = boss['Hit Points']
    damage = boss['Damage']
    mana_spent = sum(spells[spell][4] for spell in hist)
    mana_regained, recharge_available = calculate_mana_regained(hist, spells)
    mana += mana_regained - mana_spent
    hp_lost, shield_available = calculate_hp_lost(hist, spells, damage)
    hp -= hp_lost
    boss_hp_lost, poison_available = calculate_boss_hp_lost(hist, spells)
    boss_hp -= boss_hp_lost
    return mana, mana_spent, hp, boss_hp, shield_available, poison_available, recharge_available


def calculate_mana_regained(hist, spells):
    mana_regained = 5 * 101 * hist[:-2].count('re')
    recharge_available = True
    try:
        if hist[-2] == 're':
            mana_regained += 101 * 4
            recharge_available = False
    except:
        pass
    try:
        if hist[-1] == 're':
            mana_regained += 101 * 2
            recharge_available = False
    except:
        pass
    return mana_regained, recharge_available


def calculate_hp_lost(hist, spells, damage):
    hp_lost = damage * len(hist)
    hp_lost -= 2 * hist.count('dr')
    hp_lost -= 3 * max(damage - 1, 7) * hist[:-2].count('sh')
    shield_available = True
    try:
        if hist[-2] == 'sh':
            hp_lost -= 7 * 2
            shield_available = False
    except:
        pass
    try:
        if hist[-1] == 'sh':
            hp_lost -= 7 * 1
            shield_available = False
    except:
        pass
    return hp_lost, shield_available


def calculate_boss_hp_lost(hist, spells):
    boss_hp_lost = 4 * hist.count('mm')
    boss_hp_lost += 2 * hist.count('dr')
    boss_hp_lost += 6 * 3 * hist[:-2].count('po')
    poison_available = True
    try:
        if hist[-2] == 'po':
            boss_hp_lost += 3*4
            poison_available = False
    except:
        pass
    try:
        if hist[-1] == 'po':
            boss_hp_lost += 3*2
            poison_available = False
    except:
        pass
    return boss_hp_lost, poison_available


def get_next(last_attempt, shield_available, poison_available, recharge_available):
    attempt_list = [None, 'mm', 'dr', 'sh', 'po', 're']
    idx = attempt_list.index(last_attempt)
    next_attempt = attempt_list[(idx + 1) % 6]
    if shield_available == False and next_attempt == 'sh':
        next_attempt = 'po'
    if poison_available == False and next_attempt == 'po':
        next_attempt = 're'
    if recharge_available == False and next_attempt == 're':
        next_attempt = None
    return next_attempt


def min_mana(boss, spells, hard=False):
    min_mana = 25*max(spells[spell][4] for spell in spells)
    starters = ['mm', 'dr', 'sh', 'po', 're']
    for i in starters:
        hist = [i]
        last_attempt = None
        while hist:
            mana, mana_spent, hp, boss_hp, shield_available, poison_available, recharge_available = calculate_state(hist, boss, spells)
            if hard:
                hp -= len(hist)
            if mana_spent >= min_mana or hp <= 0:
                # don't care / lose
                last_attempt = hist.pop()
                continue
            elif boss_hp <= 0:
                # win
                min_mana = mana_spent
                last_attempt = hist.pop()
                continue
            elif mana < 53:
                # lose
                last_attempt = hist.pop()
                continue
            else:
                if hard:
                    hp -= 1
                    if hp <= 0:
                        # lose
                        last_attempt = hist.pop()
                        continue
                next_element = get_next(last_attempt, shield_available, poison_available, recharge_available)
                if next_element is None:
                    # tried everything, nothing works
                    last_attempt = hist.pop()
                    continue
                else:
                    hist.append(next_element)
                    last_attempt = None
                    # TODO check to make sure not too expensive + add cost of new thing to spent
                    new_cost = spells[next_element][4]
                    if new_cost > mana:
                        # too expensive--undo (but rest also too expensive)
                        hist.pop()
                        last_attempt = hist.pop()
                        continue
                    mana_spent += new_cost
                    if mana_spent >= min_mana:
                        # we've done better already
                        last_attempt = hist.pop()
                        continue
                    # work out if we kill the boss before his turn starts
                    if next_element == 'mm':
                        boss_hp -= 4
                    elif next_element == 'dr':
                        boss_hp -= 2
                    if next_element == 'po' or not(poison_available):
                        boss_hp -= 3
                    if boss_hp <= 0:
                        # win
                        min_mana = mana_spent
                        last_attempt = hist.pop()
                        continue
    return min_mana


def main():
    year, day = 2015, 22
    boss, spells = get_data(year, day)
    print(min_mana(boss, spells))
    print(min_mana(boss, spells, hard=True))


if __name__ == "__main__":
    main()
