def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [list(map(int, dimensions.split('x'))) for dimensions in data]
    return data


def total_area(data):
    return sum(individual_area(x) for x in data)


def individual_area(dimensions):
    a,b,c = dimensions
    return 2*(a*b+b*c+c*a) + min(a*b, b*c, c*a)


def total_ribbon(data):
    return sum(ribbon_length(x) for x in data)


def ribbon_length(dimensions):
    a,b,c = dimensions
    return 2*(a+b+c - max(a,b,c)) + a*b*c


def main():
    year, day = 2015, 2
    data = get_data(year, day)
    print(total_area(data))
    print(total_ribbon(data))


if __name__ == "__main__":
   main()
