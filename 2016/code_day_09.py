def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return list(data)


def decompress(data):
    idx = 0
    decompressed = []
    while idx < len(data):
        if data[idx] == '(':
            end = data.index(')', idx)
            mid = data.index('x', idx)
            repeat_times = int(''.join(data[mid + 1:end]))
            repeat_chars = int(''.join(data[idx + 1:mid]))
            for _ in range(repeat_times):
                for cell in data[end + 1:end + 1 + repeat_chars]:
                    decompressed.append(cell)
            idx = end + 1 + repeat_chars
        else:
            decompressed.append(data[idx])
            idx += 1
    return len(decompressed)


def find_last_char(char, char_list, end):
    idx = end
    while True:
        idx -= 1
        if char_list[idx] == char:
            return idx


def decompress_v2(data):
    idx = len(data) - 1
    string_from_n = [0] * (len(data) + 1)
    while idx >= 0:
        if data[idx] == ')':
            start = find_last_char('(', data, idx)
            mid = find_last_char('x', data, idx)
            repeat_times = int(''.join(data[mid + 1:idx]))
            repeat_chars = int(''.join(data[start + 1:mid]))
            a = string_from_n[idx + 1]
            b = string_from_n[idx + 1 + repeat_chars]
            string_from_n[start] = (a - b)*repeat_times + b
            idx = start - 1
        else:
            string_from_n[idx] = string_from_n[idx+1] + 1
            idx -= 1
    return string_from_n[0]


def main():
    year, day = 2016, 9
    data = get_data(year, day)
    print(decompress(data))
    print(decompress_v2(data))


if __name__ == "__main__":
    main()
