from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    instructions, image = data
    instructions = preprocess(instructions)
    image = [preprocess(datum) for datum in image.splitlines()]
    return instructions, image


def preprocess(datum):
    row = []
    for element in datum:
        if element == '#':
            row.append('1')
        else:
            row.append('0')
    return row


def enhance(instructions, image, times):
    image_dict = defaultdict(lambda: '0')
    r_max = len(image)
    c_max = len(image[0])
    for r in range(r_max):
        for c in range(c_max):
            image_dict[r, c] = image[r][c]
    for step in range(times):
        if step % 2 == 0:
            new_image_dict = defaultdict(lambda: '1')
        else:
            new_image_dict = defaultdict(lambda: '0')
        for r in range(- step - 1, r_max + step + 1):
            for c in range(- step - 1, c_max + step + 1):
                binary = []
                for r_off in range(-1, 2):
                    for c_off in range(-1, 2):
                        binary.append(image_dict[r + r_off, c + c_off])
                idx = int(''.join(binary),2)
                new_image_dict[r, c] = instructions[idx]
        image_dict = new_image_dict
    grid = []
    for r in range(- times - 2, r_max + times + 2):
        row = []
        for c in range(- times - 2, c_max + times + 2):
            row.append('#' if image_dict[r, c] == '1' else '.')
        grid.append(''.join(row))
    return sum(int(val) for val in image_dict.values())


def main():
    year, day = 2021, 20
    instructions, image = get_data(year, day)
    print(enhance(instructions, image, 2))
    print(enhance(instructions, image, 50))


if __name__ == "__main__":
    main()
