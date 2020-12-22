def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    data = [preprocess(datum) for datum in data]
    return data

def preprocess(datum):
    return list(int(i) for i in datum.splitlines()[1:])

def boring_combat(p1, p2):
    p1 = p1.copy()
    p2 = p2.copy()
    while p1 and p2:
        p1_card = p1.pop(0)
        p2_card = p2.pop(0)
        if p1_card > p2_card:
            p1.append(p1_card)
            p1.append(p2_card)
        else:
            p2.append(p2_card)
            p2.append(p1_card)
    return p1, p2

def score_combat(p1, p2):    
    if p1:
        return sum(mult*card for mult, card in zip(range(len(p1),0,-1), p1))
    else:
        return sum(mult*card for mult, card in zip(range(len(p2),0,-1), p2))

def play_boring_combat(p1, p2):
    p1, p2 = boring_combat(p1, p2)
    return score_combat(p1, p2)

def recursive_combat(p1, p2):
    p1 = p1.copy()
    p2 = p2.copy()
    SEENS = set()
    while p1 and p2:
        state = tuple(p1 + [0] + p2)
        if state in SEENS:
            return p1, p2
        else:
            SEENS.add(state)
            p1_card = p1.pop(0)
            p2_card = p2.pop(0)
            if p1_card > len(p1) or p2_card > len(p2):
                # boring case
                if p1_card > p2_card:
                    p1.append(p1_card)
                    p1.append(p2_card)
                else:
                    p2.append(p2_card)
                    p2.append(p1_card)
            else:
                # recursive combat
                rc_p1, _ = recursive_combat(p1[:p1_card], p2[:p2_card])
                if rc_p1:
                    p1.append(p1_card)
                    p1.append(p2_card)
                else:
                    p2.append(p2_card)
                    p2.append(p1_card)
    return p1, p2

def play_recursive_combat(p1, p2):
    p1, p2 = recursive_combat(p1, p2)
    return score_combat(p1, p2)

def main():
    day = 22
    p1, p2 = get_data(day)
    print(play_boring_combat(p1, p2))
    print(play_recursive_combat(p1, p2))

if __name__ == "__main__":
    main()
