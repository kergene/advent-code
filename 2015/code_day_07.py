def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = dict(create_rule(rule) for rule in data)
    return data


def create_rule(rule):
    rule = rule.split()
    target = rule[-1]
    BINARY_FUNCTIONS = ['AND', 'OR', 'RSHIFT', 'LSHIFT']
    if rule[1] in BINARY_FUNCTIONS:
        input = ([rule[0], rule[2]], rule[1])
    elif rule[0] == 'NOT':
        input = ([rule[1]], rule[0])
    else:
        input = ([rule[0]], 'IDENTITY')
    return target, input


def get_known_inputs(rules):
    known_inputs = dict()
    for input_all in rules.values():
        for input_val in input_all[0]:
            try:
                known_inputs[input_val] = int(input_val)
            except ValueError:
                pass
    return known_inputs


def apply_function(input_all, known_inputs):
    return eval(input_all[1] +'(input_all[0], known_inputs)')


def AND(input_lst, known_inputs):
    return known_inputs[input_lst[0]] & known_inputs[input_lst[1]]


def OR(input_lst, known_inputs):
    return known_inputs[input_lst[0]] | known_inputs[input_lst[1]]


def RSHIFT(input_lst, known_inputs):
    return known_inputs[input_lst[0]] >> known_inputs[input_lst[1]]


def LSHIFT(input_lst, known_inputs):
    return (known_inputs[input_lst[0]] << known_inputs[input_lst[1]]) % (2**16)


def IDENTITY(input_lst, known_inputs):
    return known_inputs[input_lst[0]]


def NOT(input_lst, known_inputs):
    return (2**16) + ~(known_inputs[input_lst[0]])


def run_gates(rules):
    known_inputs = get_known_inputs(rules)
    while 'a' not in known_inputs:
        targets_to_remove = []
        for target, input_all in rules.items():
            if set(input_all[0]).issubset(known_inputs.keys()):
                known_inputs[target] = apply_function(input_all, known_inputs)
                targets_to_remove.append(target)
        for target in targets_to_remove:
            rules.pop(target)
    return known_inputs['a']


def re_run_gates(rules, a_signal):
    known_inputs = get_known_inputs(rules)
    known_inputs['b'] = a_signal
    rules.pop('b')
    while 'a' not in known_inputs:
        targets_to_remove = []
        for target, input_all in rules.items():
            if set(input_all[0]).issubset(known_inputs.keys()):
                known_inputs[target] = apply_function(input_all, known_inputs)
                targets_to_remove.append(target)
        for target in targets_to_remove:
            rules.pop(target)
    return known_inputs['a']


def main():
    year, day = 2015, 7
    rules = get_data(year, day)
    a_signal = run_gates(rules.copy())
    print(a_signal)
    print(re_run_gates(rules, a_signal))


if __name__ == "__main__":
    main()
