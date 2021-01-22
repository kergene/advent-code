def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return data


def preprocess(datum):
    return datum


def validate(data):
    dims = [6, 25]
    layer = dims[0] * dims[1]
    min_zeros = layer
    for i in range(0, len(data), layer):
        sub = data[i:i + layer]
        if min_zeros > sub.count('0'):
            min_zeros = sub.count('0')
            one_by_two = sub.count('1') * sub.count('2')
    return one_by_two


def decode(data):
    dims = [6, 25]
    layer = dims[0] * dims[1]
    pixels = [['0' for _ in range(dims[1])] for _ in range(dims[0])]
    for i in range(len(data) - layer, -1, -layer):
        sub = data[i:i + layer]
        for r in range(dims[0]):
            for c in range(dims[1]):
                if sub[r*dims[1] + c] == '1':
                    pixels[r][c] = '1'
                elif sub[r*dims[1] + c] == '0':
                    pixels[r][c] = '0'
    for i in range(len(pixels)):
        pixels[i] = ''.join('||' if element == '1' else '  ' for element in pixels[i])
    return '\n'.join(pixels)


def main():
    year, day = 2019, 8
    data = get_data(year, day)
    print(validate(data))
    print(decode(data))


if __name__ == "__main__":
    main()
