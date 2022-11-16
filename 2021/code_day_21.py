def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return int(datum[-1])


def deterministic_dice(data):
    p1, p2 = data
    score1 = score2 = 0
    last_roll = 0
    while True:
        last_roll += 3
        p1 += 3*(last_roll - 1)
        p1 %= 10
        score1 += p1 if p1 != 0 else 10
        if score1 >= 1000:
            break
        last_roll += 3
        p2 += 3*(last_roll - 1)
        p2 %= 10
        score2 += p2 if p2 != 0 else 10
        if score2 >= 1000:
            break
    return last_roll * min(score1, score2)


class Memoize:
    def __init__(self, func):
        self.func = func
        self.memo = {}
    
    def __call__(self, state):
        if state not in self.memo:
            self.memo[state] = self.func(state)
        return self.memo[state]


@Memoize
def count_wins(state):
    ways = (1, 3, 6, 7, 6, 3, 1)
    p1, p2, score1, score2 = state
    if score1 >= 21:
        return 1, 0
    if score2 >= 21:
        return 0, 1
    wins1 = wins2 = 0
    for score in range(3, 10):
        temp_pos = (p1 + score) % 10
        temp_score = score1 + (temp_pos if temp_pos != 0 else 10)
        new_wins2, new_wins1 = count_wins((p2, temp_pos, score2, temp_score))
        wins1 += new_wins1 * ways[score - 3]
        wins2 += new_wins2 * ways[score - 3]
    return wins1, wins2


def dirac_dice(data):
    p1, p2 = data
    return max(count_wins((p1, p2, 0, 0)))


def main():
    year, day = 2021, 21
    data = get_data(year, day)
    print(deterministic_dice(data))
    print(dirac_dice(data))


if __name__ == "__main__":
    main()
