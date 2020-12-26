from math import prod
from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    bots = defaultdict(list)
    rules = dict()
    for line in data:
        line = line.split()
        if line[0] == 'value':
            bots[int(line[-1])].append(int(line[1]))
        else:
            rules[int(line[1])] = [line[5], int(line[6]), line[-2], int(line[-1])]
    return bots, rules


def which_bot(bots, rules):
    output = dict()
    check_values = set([17, 61])
    while True:
        for bot, values in bots.items():
            if len(values) != 2:
                continue
            else:
                if set(values) == check_values:
                    return bot
                bots[bot] = []
                rule = rules[bot]
                if rule[0] == 'bot':
                    bots[rule[1]].append(min(values))
                else:
                    output[rule[1]] = min(values)
                if rule[2] == 'bot':
                    bots[rule[3]].append(max(values))
                else:
                    output[rule[3]] = max(values)
                break


def get_ouputs(bots, rules):
    output = dict()
    found = True
    while found:
        found = False
        for bot, values in bots.items():
            if len(values) != 2:
                continue
            else:
                bots[bot] = []
                rule = rules[bot]
                if rule[0] == 'bot':
                    bots[rule[1]].append(min(values))
                else:
                    output[rule[1]] = min(values)
                if rule[2] == 'bot':
                    bots[rule[3]].append(max(values))
                else:
                    output[rule[3]] = max(values)
                found = True
                break
    return prod(output[i] for i in range(3))


def main():
    year, day = 2016, 10
    bots, rules = get_data(year, day)
    print(which_bot(bots, rules))
    print(get_ouputs(bots, rules))


if __name__ == "__main__":
    main()
