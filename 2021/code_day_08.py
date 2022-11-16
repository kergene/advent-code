from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    signals, outputs = datum.split(' | ')
    return signals.split(), outputs.split()


def count_1478(data):
    count = 0
    for row in data:
        _, outputs = row
        for digit in outputs:
            if len(digit) in (2, 3, 4, 7):
                count += 1
    return count


def sum_decoded(data):
    total = 0
    for row in data:
        total += decode(row)
    return total


def decode(row):
    signals, outputs = row
    signal_lengths = defaultdict(list)
    for signal in signals:
        signal_lengths[len(signal)].append(set(signal))
    one = signal_lengths[2][0]
    four = signal_lengths[4][0]
    seven = signal_lengths[3][0]
    eight = signal_lengths[7][0]
    top = seven - one
    upper_left_middle = four - one
    lower_left_bottom = eight - four - top
    for digit in signal_lengths[6]:
        if len(one - digit) == 1:
            upper_right = one - digit
            lower_right = one - upper_right
            break
    for digit in signal_lengths[5]:
        if len(one - digit) == 0:
            middle = digit - seven - lower_left_bottom
            upper_left = upper_left_middle - middle
            bottom = digit - seven - middle
            lower_left = lower_left_bottom - bottom
            break
    all_encodings = set('abcdefg')
    zero = all_encodings - middle
    two = all_encodings - upper_left - lower_right
    three = all_encodings - upper_left - lower_left
    five = all_encodings - upper_right - lower_left
    six = all_encodings - upper_right
    nine = all_encodings - lower_left
    numbers = [zero, one, two, three, four, five, six, seven, eight, nine]
    out = []
    for digit in outputs:
        digit = set(digit)
        for index, number_set in enumerate(numbers):
            if digit == number_set:
                out.append(str(index))
                break
    return int(''.join(out))


def main():
    year, day = 2021, 8
    data = get_data(year, day)
    print(count_1478(data))
    print(sum_decoded(data))


if __name__ == "__main__":
    main()
