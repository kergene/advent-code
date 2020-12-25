import re


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return data


def count_numbers(data):
    a = re.findall('(-?[0-9]+)', data)
    return sum(int(i) for i in a)


def count_no_reds(data):
    a = eval(data)
    return recurse_reds(a)


def recurse_reds(a):
    if isinstance(a, list):
        b = [recurse_reds(sub) for sub in a]
        return sum(score for score in b if score != "red")
    elif isinstance(a, dict):
        b = [recurse_reds(sub) for sub in a.values()]
        if 'red' not in b:
            return sum(b)
        else:
            return 0
    elif isinstance(a, str):
        if a == "red":
            return "red"
        else:
            return 0
    elif isinstance(a, int):
        return(a)
    else:
        print(type(a))
        raise TypeError('type')


def main():
    year, day = 2015, 12
    data = get_data(year, day)
    print(count_numbers(data))
    print(count_no_reds(data))


if __name__ == "__main__":
    main()
