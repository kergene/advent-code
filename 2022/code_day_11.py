import sys
from pathlib import Path
from collections import defaultdict
from queue import SimpleQueue

sys.path.append(str(Path(__file__).parent.parent))
import import_data

def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().split('\n\n')
    return data


def preprocess(datum):
    datum = datum.splitlines()
    number = int(datum[0][-2])
    items = datum[1].split(': ')[1]
    items = [int(val) for val in items.split(', ')]
    new_items = SimpleQueue()
    for item in items:
        new_items.put(item)
    ops = datum[2].split('= ')[1].split()
    ops = [int(val) if val not in ('*', '+', 'old') else val for val in ops]
    divs = int(datum[3].split(' by ')[1])
    if_true = int(datum[4].split(' monkey ')[1])
    if_false = int(datum[5].split(' monkey ')[1])
    return number, new_items, ops, divs, if_true, if_false


def monkey_in_the_middle(data):
    data = [preprocess(datum) for datum in data]
    inspected = defaultdict(int)
    for _ in range(20):
        for monkey_number, items, ops, divs, if_true, if_false in data:
            while not items.empty():
                item = items.get()
                inspected[monkey_number] += 1
                if ops[1] == '+':
                    item += ops[2]
                elif ops[1] == '*':
                    if ops[2] == 'old':
                        item *= item
                    else:
                        item *= ops[2]
                item //= 3
                if item % divs == 0:
                    data[if_true][1].put(item)
                else:
                    data[if_false][1].put(item)
    vals = sorted(inspected.values())
    return vals[-1] * vals[-2]


def monkey_panic(data):
    data = [preprocess(datum) for datum in data]
    inspected = defaultdict(int)
    mod_num = 1
    for monkey in data:
        mod_num *= monkey[3]
    for _ in range(10000):
        for monkey_number, items, ops, divs, if_true, if_false in data:
            while not items.empty():
                item = items.get()
                inspected[monkey_number] += 1
                if ops[1] == '+':
                    item += ops[2]
                elif ops[1] == '*':
                    if ops[2] == 'old':
                        item *= item
                    else:
                        item *= ops[2]
                item %= mod_num
                if item % divs == 0:
                    data[if_true][1].put(item)
                else:
                    data[if_false][1].put(item)
    vals = sorted(inspected.values())
    return vals[-1] * vals[-2]


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(monkey_in_the_middle(data))
    print(monkey_panic(data))


if __name__ == "__main__":
    main()
