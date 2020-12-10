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

def get_data():
    with open("input_day_2.txt") as f:
        data = f.read()
    data = data.splitlines()
    return data
    

if __name__ == "__main__":
    data = get_data()
    rule_1_truths = [check_password_1(i) for i in data]
    print(sum(rule_1_truths))
    rule_2_truths = [check_password_2(i) for i in data]
    print(sum(rule_2_truths))
