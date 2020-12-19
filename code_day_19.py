from collections import defaultdict
from itertools import product

def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    rules = dict(preprocess(datum) for datum in data[0].splitlines())
    messages = data[1].splitlines()
    inv_t_p, inv_nt_p, n_nt = cnf(rules)
    return inv_t_p, inv_nt_p, n_nt, messages

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
    nt_prods = dict()
    t_prods = dict()
    n_nt = 0
    for rule_idx, output in rules.items():
        if rule_idx > n_nt:
            n_nt = rule_idx
        if len(output[0]) == 1:
            t_prods[rule_idx] = output
        else:
            nt_prods[rule_idx] = output
    inv_t_p, inv_nt_p = invert_rules(t_prods, nt_prods)
    return inv_t_p, inv_nt_p, n_nt

def invert_rules(t_prods, nt_prods):
    # inverts rule dictionaries for performance
    inv_t_p = defaultdict(set)
    for nonterminal, outputs in t_prods.items():
        for production in outputs:
            inv_t_p[production[0]].add(nonterminal)
    inv_nt = defaultdict(set)
    for nonterminal, outputs in nt_prods.items():
        for production in outputs:
            inv_nt[tuple(production)].add(nonterminal)
    return inv_t_p, inv_nt

def cyk(string, inv_t, inv_nt):
    # runs CYK algorithm
    n = len(string)
    M = [[set() for _ in range(n)] for _ in range(n)]
    for i in range(len(string)):
        for nonterminal in inv_t[string[i]]:
            M[i][i].add(nonterminal)
    for length in range(1, n):
        for start in range(0, n - length):
            for partition in range(0, length):
                L = M[start][start + partition]
                R = M[start + partition + 1][start + length]
                for nt_prod in product(L, R):
                    for A in inv_nt[nt_prod]:
                        M[start][start + length].add(A)
    return 0 in M[0][-1]

def easy_cnf(inv_t_p, inv_nt_p, messages):
    tot = 0
    for line in messages:
        tot += cyk(line, inv_t_p, inv_nt_p)
    return tot

def add_nt_rules(inv_nt_p, n_nt, extra_nt_p):
    # adds slightly more complex rules to inverted cnf
    for nonterminal, outputs in extra_nt_p.items():
        for production in outputs:
            while len(production) > 2:
                n_nt += 1
                inv_nt_p[tuple(production[-2:])].add(n_nt)
                production = production[:-1]
                production[-1] = n_nt
            inv_nt_p[tuple(production)].add(nonterminal)
    return inv_nt_p

def harder_cnf(inv_t_p, inv_nt_p, n_nt, messages):
    extra_nt_p = dict()
    extra_nt_p[8] = [[42, 8]]
    extra_nt_p[11] = [[42, 11, 31]]
    inv_nt_p = add_nt_rules(inv_nt_p, n_nt, extra_nt_p)
    return easy_cnf(inv_t_p, inv_nt_p, messages)

def main():
    day = 19
    inv_t_p, inv_nt_p, n_nt, messages = get_data(day)
    print(easy_cnf(inv_t_p, inv_nt_p, messages))
    print(harder_cnf(inv_t_p, inv_nt_p, n_nt, messages))

if __name__ == "__main__":
    main()
