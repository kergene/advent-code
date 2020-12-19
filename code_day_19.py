def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    rules = dict(preprocess(datum) for datum in data[0].splitlines())
    messages = data[1].splitlines()
    return rules, messages

def preprocess(datum):
    datum = datum.split(':')
    base = int(datum[0])
    datum = datum[1].split('|')
    options = []
    for choice in datum:
        if '"' in choice:
            options.append([choice[2]])
        else:
            options.append([int(val) for val in choice.split()])
    return base, options

def cnf(rules):
    # converts the grammar to CNF
    #     only deals with basic cases from input
    found = True
    while found:
        found = False
        for base, outputs in rules.items():
            if len(outputs[0]) == 1:
                new_outputs = []
                for i in range(len(outputs)):
                    choice = outputs[i]
                    if choice[0] not in ('a', 'b'):
                        for j in rules[choice[0]]:
                            new_outputs.append(j)
                        found = True
                    else:
                        new_outputs.append([choice[0]])
                rules[base] = new_outputs
    nonterminal_rules = dict()
    terminal_rules = dict()
    max_idx = 0
    for rule_idx, output in rules.items():
        if rule_idx > max_idx:
            max_idx = rule_idx
        if len(output[0]) == 1:
            terminal_rules[rule_idx] = output
        else:
            nonterminal_rules[rule_idx] = output
    return terminal_rules, nonterminal_rules, max_idx

def cyk(string, terminal_rules, nonterminal_rules, r):
    # runs CYK algorithm
    n = len(string)
    M = [[set() for _ in range(n)] for _ in range(n)]
    for i in range(len(string)):
        for T, terminal_choices in terminal_rules.items():
            for terminal in terminal_choices:
                if string[i] == terminal[0]:
                    M[i][i].add(T)
    for length in range(1, n):
        for start in range(0, n - length):
            for partition in range(0, length):
                L = M[start][start + partition]
                R = M[start + partition + 1][start + length]
                for A, nonterminal_choices in nonterminal_rules.items():
                    for B, C in nonterminal_choices:
                        if B in L and C in R:
                            M[start][start + length].add(A)
    return 0 in M[0][-1]

def easy_cnf(rules, messages):
    terminal_rules, nonterminal_rules, max_idx = cnf(rules)
    tot = 0
    for line in messages:
        tot += cyk(line, terminal_rules, nonterminal_rules, max_idx)
    return tot

def add_nt_rules(nonterminal_rules, max_idx, extra_nt_rules):
    # adds slightly more complex rules to CNF
    for nonterminal, outputs in extra_nt_rules.items():
        for output in outputs:
            if len(output) == 2:
                nonterminal_rules[nonterminal].append(output)
            else:
                while len(output) > 2:
                    nonterminal_rules[max_idx + 1] = [output[-2:]]
                    output = output[:-1]
                    output[-1] = max_idx + 1
                    max_idx += 1
                nonterminal_rules[nonterminal].append(output)
    return nonterminal_rules, max_idx

def harder_cnf(rules, messages):
    extra_nt_rules = dict()
    extra_nt_rules[8] = [[42, 8]]
    extra_nt_rules[11] = [[42, 11, 31]]
    terminal_rules, nonterminal_rules, max_idx = cnf(rules)
    nonterminal_rules, max_idx = add_nt_rules(nonterminal_rules, max_idx, extra_nt_rules)
    tot = 0
    for line in messages:
        tot += cyk(line, terminal_rules, nonterminal_rules, max_idx)
    return tot

def main():
    day = 19
    rules, messages = get_data(day)
    print(easy_cnf(rules, messages))
    print(harder_cnf(rules, messages))

if __name__ == "__main__":
    main()
