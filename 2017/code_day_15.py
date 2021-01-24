def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return int(datum.split()[-1])


def gen_next(gen, mult, mod, rule):
    gen *= mult
    gen %= mod
    if gen % rule == 0:
        return gen
    else:
        return gen_next(gen, mult, mod, rule)


def gen_values(data, repeats, a_rule, b_rule):
    a_mult = 16807
    b_mult = 48271
    mod = 2147483647
    a_gen = data[0]
    b_gen = data[1]
    matches = 0
    for _ in range(repeats):
        a_gen = gen_next(a_gen, a_mult, mod, a_rule)
        b_gen = gen_next(b_gen, b_mult, mod, b_rule)
        if (a_gen - b_gen) % 65536 == 0:
            matches += 1
    return matches


def main():
    year, day = 2017, 15
    data = get_data(year, day)
    print(gen_values(data, 4 * 10 ** 7, 1, 1))
    print(gen_values(data, 5 * 10 ** 6, 4, 8))


if __name__ == "__main__":
    main()
