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
    q, seens = set(("shiny gold",)), set()
    while q:
        test_bag = q.pop()
        for outer_bag, inner_bags in rules.items():
            if test_bag in inner_bags and outer_bag not in seens:
                q.add(outer_bag)
                seens.add(outer_bag)
    return len(seens)


def count_inner_bags(rules):
    known_inners = dict((outer_bag, 0) for outer_bag, inner_bags in rules.items() if not inner_bags)
    for bag in known_inners:
        rules.pop(bag)
    while "shiny gold" not in known_inners:
        rules_to_remove = []
        for outer_bag, inner_bag_dict in rules.items():
            if set(inner_bag_dict.keys()).issubset(known_inners.keys()):
                known_inners[outer_bag] = sum(colour_count * (known_inners[bag_colour] + 1) for bag_colour, colour_count in inner_bag_dict.items())
                rules_to_remove.append(outer_bag)
        for outer_bag in rules_to_remove:
            rules.pop(outer_bag)
    return known_inners["shiny gold"]


def main():
    year, day = 2020, 7
    rules = get_data(year, day)
    print(find_outer_bags(rules))
    print(count_inner_bags(rules))


if __name__ == "__main__":
    main()
