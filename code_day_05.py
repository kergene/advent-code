from itertools import product

def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data

def seat_id(string):
    REPLACE = {'F':'0',
               'B':'1',
               'L':'0',
               'R':'1'}
    for old, new in REPLACE.items():
        string = string.replace(old, new)
    return int(string, 2)

def check_cards(data):
    data = [seat_id(i) for i in data]
    return max(data)

def find_card(data):
    A = 'FB'
    B = 'LR'
    flag = 0
    for lst in product(A, A, A, A, A, A, A, B, B, B):
        if ''.join(lst) not in data:
            if flag:
                return seat_id(''.join(lst))
        else:
            flag = 1

def main():
    day = 5
    data = get_data(day)
    print(check_cards(data))
    print(find_card(data))

if __name__ == "__main__":
    main()
