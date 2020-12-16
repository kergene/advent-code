from collections import defaultdict
from math import prod

def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    rules = data[0]
    rules = dict(preprocess_rule(datum) for datum in rules.splitlines())
    me = data[1]
    me = preprocess_ticket(me.splitlines()[1])
    others = data[2]
    others = [preprocess_ticket(datum) for datum in others.splitlines()[1:]]
    return rules, me, others

def preprocess_rule(datum):
    datum = datum.split(':')
    key = datum[0]
    value = datum[1].split()
    bounds = value[0].split('-') + value[2].split('-')
    bounds = [int(i) for i in bounds]
    return key, bounds

def preprocess_ticket(datum):
    return [int(i) for i in datum.split(',')]

def remove_invalid(rules, me, others):
    total = 0
    keep = []
    for ticket in others:
        keep_ticket = True
        for field in ticket:
            valid_field = False
            for bounds in rules.values():
                if bounds[0] <= field <= bounds[1]:
                    valid_field = True
                    break
                elif bounds[2] <= field <= bounds[3]:
                    valid_field = True
                    break
            if not valid_field:
                total += field
                keep_ticket = False
        if keep_ticket:
            keep.append(ticket)
    return total, keep

def identity_fields(rules, me, others):
    n_tickets = len(others)
    groups = list(zip(*others))
    n_fields = len(groups)
    # create dict of sets of possible fields (by column)
    links = defaultdict(set)
    for i in range(n_fields):
        group = groups[i]
        for field, bounds in rules.items():
            n_valid = sum(1 for value in group if bounds[0] <= value <= bounds[1] or bounds[2] <= value <= bounds[3])
            if n_valid == n_tickets:
                links[field].add(i)
    # loop over fields: check if can say what field somehting is
    fixed_links = {}
    while len(fixed_links) < n_fields:
        for field, possibles in links.items():
            if len(possibles) == 1:
                known_value = possibles.pop()
                fixed_links[field] = known_value
                # removes found field from everywhere else
                for other_field, other_possibles in links.items():
                    if known_value in other_possibles:
                        links[other_field].remove(known_value)
    # return product of fields with 'departure' in
    return prod(me[column] for field, column in fixed_links.items() if 'departure' in field)

def main():
    day = 16
    rules, me, others = get_data(day)
    error_rate, others = remove_invalid(rules, me, others)
    print(error_rate)
    print(identity_fields(rules, me, others))

if __name__ == "__main__":
    main()
