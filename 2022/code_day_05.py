import sys
from pathlib import Path
from queue import LifoQueue

sys.path.append(str(Path(__file__).parent.parent))
import import_data


def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().split('\n\n')
    stacks = list(list(val) for val in data[0].splitlines())
    stacks = list(zip(*stacks))
    stacks = [preprocess(datum) for datum in stacks[1:]]
    stacks = [val for val in stacks if val is not None]
    stacks = list(zip(*stacks))
    lines = [preprocess_lines(datum) for datum in data[1].splitlines()]
    return stacks, lines


def preprocess(datum):
    # create two stacks as stacks are mutable (and cannot be copied)
    datum = list(datum)
    datum.reverse()
    if datum[0] not in '123456789':
        return None
    stack = LifoQueue()
    stack2 = LifoQueue()
    for val in datum[1:]:
        if val == ' ':
            break
        stack.put(val)
        stack2.put(val)
    return stack, stack2


def preprocess_lines(datum):
    datum = datum.split(' ')
    crate_count = int(datum[1])
    from_idx = int(datum[3])
    to_idx = int(datum[5])
    return crate_count, from_idx, to_idx


def crate_mover_9000(data):
    stacks, lines = data
    stacks = stacks[0]
    for row in lines:
        crate_count, from_idx, to_idx = row
        for _ in range(crate_count):
            new = stacks[from_idx - 1].get()
            stacks[to_idx - 1].put(new)
    total = []
    for stack in stacks:
        total.append(stack.get())
    return ''.join(total)


def crate_mover_9001(data):
    stacks, lines = data
    stacks = stacks[1]
    for row in lines:
        crate_count, from_idx, to_idx = row
        temp_stack = LifoQueue()
        for _ in range(crate_count):
            new = stacks[from_idx - 1].get()
            temp_stack.put(new)
        for _ in range(crate_count):
            new = temp_stack.get()
            stacks[to_idx - 1].put(new)
    total = []
    for stack in stacks:
        total.append(stack.get())
    return ''.join(total)


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(crate_mover_9000(data))
    print(crate_mover_9001(data))


if __name__ == "__main__":
    main()
