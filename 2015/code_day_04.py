import hashlib


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return data


def mine_star(message, leading_zeros):
    zeros = '0' * leading_zeros
    i = 1
    while True:
        input = message + str(i)
        hashed = hashlib.md5(input.encode('utf-8')).hexdigest()
        if hashed[:leading_zeros] == zeros:
            return i
        i += 1


def main():
    year, day = 2015, 4
    message = get_data(year, day)
    print(mine_star(message, 5))
    print(mine_star(message, 6))


if __name__ == "__main__":
    main()
