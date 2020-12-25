def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return data


def brackets(data):
    return data.count('(') - data.count(')')


def basement_index(data):
    counter = 0
    for i in range(len(data)):
        if data[i] == '(':
            counter += 1
        else:
            counter -= 1
            if counter < 0:
                return i + 1


def main():
    year, day = 2015, 1
    data = get_data(year, day)
    print(brackets(data))
    print(basement_index(data))


if __name__ == "__main__":
   main()
