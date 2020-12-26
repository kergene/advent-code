def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def process_string(text):
    rule, letter, word = text.split()
    rule = [int(i) for i in rule.split('-')]
    letter = letter[0]
    return rule, letter, word


def check_password_counting(text):
    rule, letter, word = process_string(text)
    counter = word.count(letter)
    return counter >= rule[0] and counter <= rule[1]


def check_password_indexing(text):
    rule, letter, word = process_string(text)
    return (word[rule[0] - 1] == letter) ^ (word[rule[1] - 1] == letter)


def main():
    year, day = 2020, 2
    data = get_data(year, day)
    rule_1_truths = [check_password_counting(i) for i in data]
    print(sum(rule_1_truths))
    rule_2_truths = [check_password_indexing(i) for i in data]
    print(sum(rule_2_truths))


if __name__ == "__main__":
    main()
