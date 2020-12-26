def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [int(i) for i in data]
    data.append(0)
    data.sort()
    data.append(data[-1] + 3)
    return data


def find_gaps(data):
    # note gaps are always of length 1 or 3
    m = data[-1]
    gaps = len(data) - 1
    threes = (m - gaps) // 2
    ones = gaps - threes
    return ones * threes


def count_ways(data):
    product = 1
    last_three_idx = 0
    for i in range(len(data)):
        if data[i] - data[i-1] == 3:
            product *= three_term_fib(i - last_three_idx)
            last_three_idx = i
    return product


def three_term_fib(n):
    # have n numbers, can go up by 1,2,3 numbers at time
    if n == 1: return 1
    if n == 2: return 1
    a, b, c = 0, 1, 1
    for _ in range(n-2):
        c, b, a = a+b+c, c, b
    return c


def main():
    year, day = 2020, 10
    data = get_data(year, day)
    print(find_gaps(data))
    print(count_ways(data))   


if __name__ == "__main__":
    main()
