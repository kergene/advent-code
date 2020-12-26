import hashlib


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return data


def crack_password(data):
    password = []
    i = 0
    found = 0
    while found < 8:
        i += 1
        attempt = data + str(i)
        hashed = hashlib.md5(attempt.encode('utf-8')).hexdigest()
        if hashed[:5] == '00000':
            password.append(hashed[5])
            found += 1
    return ''.join(password)


def crack_password_hard(data):
    password = ['0'] * 8
    i = 0
    unfound = set(str(i) for i in range(8))
    while unfound:
        i += 1
        attempt = data + str(i)
        hashed = hashlib.md5(attempt.encode('utf-8')).hexdigest()
        if hashed[:5] == '00000':
            if hashed[5] in unfound:
                password[int(hashed[5])] = hashed[6]
                unfound.remove(hashed[5])
    return ''.join(password)


def main():
    year, day = 2016, 5
    data = get_data(year, day)
    print(crack_password(data))
    print(crack_password_hard(data))


if __name__ == "__main__":
    main()
