def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    data = list(ord(i) for i in data)
    return data


def next_password(password):
    index = -1
    found = False
    while not found:
        password[index] += 1
        if password[index] == 123:
            password[index] = 97
            index -= 1
        elif password[index] in (105, 108, 111):
            continue
        else:
            return password


def password_illegal_check(password):
    subtracted = [password[i] - password[i-1] for i in range(1, len(password))]
    found_triple = False
    i = 0
    while i < len(subtracted) - 1:
        if subtracted[i] == subtracted[i+1] == 1:
            found_triple = True
            break
        i += 1
    found_doubles = 0
    i = 0
    while i < len(subtracted):
        if subtracted[i] == 0:
            found_doubles += 1
            i += 2
            if found_doubles == 2:
                break
        i += 1
    return not((found_doubles == 2) and found_triple)


def next_valid_password(password):
    illegal = True
    while illegal:
        password = next_password(password)
        illegal = password_illegal_check(password)
    return password, ''.join([chr(i) for i in password])


def main():
    year, day = 2015, 11
    password = get_data(year, day)
    password, str_password = next_valid_password(password)
    print(str_password)
    password, str_password = next_valid_password(password)
    print(str_password)


if __name__ == "__main__":
    main()
