import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import import_data

class Memoize:
    def __init__(self, func):
        self.func = func
        self.memo = {}

    def __call__(self, state, data):
        if state not in self.memo:
            self.memo[state] = self.func(state, data)
        return self.memo[state]

    def clear(self):
        self.memo.clear()


def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    data = dict(preprocess(datum) for datum in data)
    return data


def preprocess(datum):
    shout, listen = datum.split(': ')
    listen = listen.split(' ')
    return shout, listen


@Memoize
def shout_recursive_double(shout, data):
    if isinstance(shout, int):
        return shout, True
    listen = data[shout]
    if len(listen) == 1:
        return int(listen[0]), shout != 'humn'
    assert len(listen) == 3
    listen_first, pass_first =  shout_recursive_double(listen[0], data)
    listen_second, pass_second =  shout_recursive_double(listen[2], data)
    if listen[1] == '*':
        math_result = listen_first * listen_second
    elif listen[1] == '/':
        math_result = listen_first // listen_second
    elif listen[1] == '-':
        math_result = listen_first - listen_second
    elif listen[1] == '+':
        math_result = listen_first + listen_second
    else:
        assert False
    return math_result, (pass_first and pass_second)


def part_1(data):
    target = 'root'
    return shout_recursive_double(target, data)[0]


def part_2(data):
    knowns = {}
    unknowns = {}
    for target in data.keys():
        math, known = shout_recursive_double(target, data)
        if known:
            knowns[target] = math
        else:
            unknowns[target] = data[target]
    unknowns['root'][1] = '='
    del unknowns['humn']
    # fix known values
    for value in unknowns.values():
        for idx in (0, 2):
            if value[idx] in knowns:
                value[idx] = knowns[value[idx]]
    # invert rules
    reversed_rules = dict(invert_row(key, value) for key, value in unknowns.items())
    # reset memoization
    shout_recursive_double.clear()
    # redo evaluation
    return shout_recursive_double('humn', reversed_rules)[0]


def invert_row(key, value):
    # rearrange equation
    if value[1] == '/':
        if isinstance(value[0], str):
            return value[0], [key, '*', value[2]]
        return value[2], [value[0], '/', key]
    if value[1] == '-':
        if isinstance(value[0], str):
            return value[0], [key, '+', value[2]]
        return value[2], [value[0], '-', key]
    # plus/times are order independent
    if isinstance(value[0], str):
        unknown = value[0]
        known = value[2]
    else:
        unknown = value[2]
        known = value[0]
    if value[1] == '*':
        return unknown, [key, '/', known]
    if value[1] == '+':
        return unknown, [key, '-', known]
    if value[1] == '=':
        return unknown, [known]
    assert False


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(data)
    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
