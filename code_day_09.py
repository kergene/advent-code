from itertools import combinations

def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [int(i) for i in data]
    return data

def find_invalid(data):
    for i in range(25,len(data)):
        test = data[i]
        pre_set = data[i-25:i]
        flag = False
        for i, j in combinations(pre_set,2):
            if i + j == test:
                flag = True
                break
        if not flag:
            return test

def find_continuous_sum(data, target):
    set_len = 2
    while True:
        for i in range(len(data) - set_len + 1):
            if sum(data[i:i + set_len]) == target:
                return max(data[i:i + set_len]) + min(data[i:i + set_len])
        set_len += 1

def main():
    day = 9
    data = get_data(day)
    p1 = find_invalid(data)
    print(p1)
    print(find_continuous_sum(data, p1))     

if __name__ == "__main__":
    main()
