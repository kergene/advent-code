def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return int(data)


def chocolate_scores(data):
    current_a = 0
    current_b = 1
    board = [3, 7]
    board_len = 2
    while board_len < data + 10:
        new = board[current_a] + board[current_b]
        for digit in str(new):
            board.append(int(digit))
            board_len += 1
        current_a += board[current_a] + 1
        current_a %= board_len
        current_b += board[current_b] + 1
        current_b %= board_len
    return ''.join(str(i) for i in board[data:data + 10])


def recipes_needed(data):
    data = list(int(i) for i in str(data))
    n = len(data)
    current_a = 0
    current_b = 1
    board = [3, 7]
    board_len = 2
    check_idx = 0
    while True:
        new = board[current_a] + board[current_b]
        for digit in str(new):
            board.append(int(digit))
            board_len += 1
        current_a += board[current_a] + 1
        current_a %= board_len
        current_b += board[current_b] + 1
        current_b %= board_len
        while check_idx + n <= board_len:
            if board[check_idx:check_idx + n] == data:
                return check_idx
            else:
                check_idx += 1


def main():
    year, day = 2018, 14
    data = get_data(year, day)
    print(chocolate_scores(data))
    print(recipes_needed(data))


if __name__ == "__main__":
    main()
