def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def nice_count(strings):
    return sum(nice_string(example) for example in strings)


def nice_string(example):
    vowels = 'aeiou'
    doubles = [chr(i)*2 for i in range(ord('a'), ord('z')+1)]
    forbidden =  ['ab', 'cd', 'pq', 'xy']
    count = 0
    for i in vowels:
        count += example.count(i)
    count_allowed = count >= 3
    found_double = False
    for i in doubles:
        if i in example:
            found_double = True
            break
    found_forbidden = False
    for i in forbidden:
        if i in example:
            found_forbidden = True
            break
    return count_allowed and found_double and not found_forbidden


def new_nice_count(strings):
    return sum(new_nice_string(example) for example in strings)


def new_nice_string(example):
    found_split = False
    for idx in range(len(example) - 2):
        if example[idx+2] == example[idx]:
            found_split = True
            break
    found_pair = False
    for idx in range(len(example) - 3):
        test_pair = example[idx:idx+2]
        for other in range(idx + 2, len(example) - 1):
            if test_pair == example[other:other+2]:
                found_pair = True
                break
    return found_split and found_pair


def main():
    year, day = 2015, 5
    strings = get_data(year, day)
    print(nice_count(strings))
    print(new_nice_count(strings))


if __name__ == "__main__":
    main()
