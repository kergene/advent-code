from itertools import permutations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    datum = datum.replace('[', ' ').replace(']', ' ')
    datum = datum.split()
    d = {'allowed': [], 'disallowed': []}
    for i in range(len(datum)):
        if i % 2 == 0:
            d['allowed'].append(datum[i])
        else:
            d['disallowed'].append(datum[i])
    return d


def contains_abba(string_list):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for string in string_list:
        for i, j in permutations(alphabet, 2):
            if ''.join([i,j,j,i]) in string:
                return True
    return False


def tls_finder(data):
    count = 0
    for line in data:
        if contains_abba(line['allowed']) and not contains_abba(line['disallowed']):
            count += 1
    return count


def contains_aba(string_list):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    abas = []
    for string in string_list:
        for i, j in permutations(alphabet, 2):
            if ''.join([i,j,i]) in string:
                abas.append([i,j])
    return abas


def contains_bab(string_list, abas):
    for string in string_list:
        for i, j in abas:
            if ''.join([j,i,j]) in string:
                return True
    return False


def ssl_finder(data):
    count = 0
    for line in data:
        contents = contains_aba(line['allowed'])
        if contents:
            if contains_bab(line['disallowed'], contents):
                count += 1
    return count


def main():
    year, day = 2016, 7
    data = get_data(year, day)
    print(tls_finder(data))
    print(ssl_finder(data))


if __name__ == "__main__":
    main()
