def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def check_password_1(text):
    rule, letter, word = text.split()
    rule = list(map(int, rule.split('-')))
    counter = word.count(letter[0])
    if counter >= rule[0] and counter <= rule[1]:
        return True
    else:
        return False


def check_password_2(text):
    rule, letter, word = text.split()
    rule = list(map(int, rule.split('-')))
    letter = letter[0]
    if (word[rule[0] - 1] == letter) != (word[rule[1] - 1] == letter):
        return True
    else:
        return False


def main():
    year, day = 2020, 2
    data = get_data(year, day)
    rule_1_truths = [check_password_1(i) for i in data]
    print(sum(rule_1_truths))
    rule_2_truths = [check_password_2(i) for i in data]
    print(sum(rule_2_truths))


if __name__ == "__main__":
    main()
