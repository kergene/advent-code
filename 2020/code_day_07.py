from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = dict(create_rule(rule) for rule in data)
    return data


def create_rule(rule):
    rule = rule.split(' bag')
    rule.pop()
    outer_bag = rule[0]
    inner_bags = dict((' '.join(bag.split()[-2:]),int(bag.split()[-3])) for bag in rule[1:] if "no other" not in bag)
    return outer_bag, inner_bags


def find_outer_bags(rules):
    reverse_rules = defaultdict(set)
    for outer_bag, inner_bags in rules.items():
        for bag in inner_bags:
            reverse_rules[bag].add(outer_bag)
    TARGET = "shiny gold"
    q, seens = set((TARGET,)), set()
    while q:
        test_bag = q.pop()
        for outer_bag in reverse_rules[test_bag]:
            if outer_bag not in seens:
                q.add(outer_bag)
                seens.add(outer_bag)
    return len(seens)


class Memoize:
    def __init__(self, func):
        self.func = func
        self.memo = {}
    
    def __call__(self, bag, rules):
        if bag not in self.memo:
            self.memo[bag] = self.func(bag, rules)
        return self.memo[bag]


@Memoize
def count_inner_bags_recursive(bag, rules):
    return sum(colour_count * (count_inner_bags_recursive(inner_bag, rules) + 1) for inner_bag, colour_count in rules[bag].items())


def main():
    year, day = 2020, 7
    rules = get_data(year, day)
    print(find_outer_bags(rules))
    print(count_inner_bags_recursive('shiny gold', rules))


if __name__ == "__main__":
    main()
