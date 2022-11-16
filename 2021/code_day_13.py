def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        dots, instructions = f.read().split('\n\n')
    dots = [preprocess(datum) for datum in dots.split()]
    instructions = [preprocess_instructions(datum) for datum in instructions.splitlines()]
    return dots, instructions


def preprocess(datum):
    return tuple(int(val) for val in datum.split(','))


def preprocess_instructions(datum):
    datum = datum.split()[-1]
    coord, val = datum.split('=')
    return coord, int(val)


def fold_once(dots, instructions):
    row = instructions[0]
    new_dots = set()
    if row[0] == 'x':
        for x, y in dots:
            if x < row[1]:
                new_dots.add((x, y))
            else:
                new_dots.add((2*row[1] - x, y))
    else:
        for x, y in dots:
            if y < row[1]:
                new_dots.add((x, y))
            else:
                new_dots.add((x, 2*row[1] - y))
    return len(new_dots)


def fold_fully(dots, instructions):
    dots = set(dots)
    for row in instructions:
        new_dots = set()
        if row[0] == 'x':
            for x, y in dots:
                if x < row[1]:
                    new_dots.add((x, y))
                else:
                    new_dots.add((2*row[1] - x, y))
        else:
            for x, y in dots:
                if y < row[1]:
                    new_dots.add((x, y))
                else:
                    new_dots.add((x, 2*row[1] - y))
        dots = new_dots
    max_x = max(dot[0] for dot in dots) + 1
    max_y = max(dot[1] for dot in dots) + 1
    rows = []
    for y in range(max_y):
        rows.append(''.join('##' if (x,y) in dots else '  ' for x in range(max_x)))
    return '\n'.join(rows)


def main():
    year, day = 2021, 13
    dots, instructions = get_data(year, day)
    print(fold_once(dots, instructions))
    print(fold_fully(dots, instructions))


if __name__ == "__main__":
    main()
