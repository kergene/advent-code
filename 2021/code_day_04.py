def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    calls, calls_dict = preprocess_calls(data[0])
    boards = [preprocess(datum) for datum in data[1:]]
    return calls, calls_dict, boards


def preprocess_calls(data):
    calls = [int(num) for num in data.split(',')]
    calls_dict = dict((val, pos) for pos, val in enumerate(calls))
    return calls, calls_dict


def preprocess(datum):
    return [[int(num) for num in row.split()] for row in datum.splitlines()]


def calculate_board(calls, calls_dict, board):
    length = 0
    score = 1
    corrected_board = []
    for row in board:
        corrected_row = []
        for element in row:
            corrected_row.append(calls_dict[element])
        corrected_board.append(corrected_row)
    best_row = min(max(row) for row in corrected_board)
    best_col = min(max(row) for row in zip(*corrected_board))
    length = min(best_row, best_col)
    board_vals = set(element for row in board for element in row)
    called = set(calls[:length + 1])
    score = sum(board_vals - called) * calls[length]
    return length, score


def win_bingo(calls, calls_dict, boards):
    best_length = 100
    best_score = None
    for board in boards:
        length, score = calculate_board(calls, calls_dict, board)
        if length < best_length:
            best_score = score
            best_length = length
    return best_score


def lose_bingo(calls, calls_dict, boards):
    best_length = 0
    best_score = None
    for board in boards:
        length, score = calculate_board(calls, calls_dict, board)
        if length > best_length:
            best_score = score
            best_length = length
    return best_score


def main():
    year, day = 2021, 4
    calls, calls_dict, boards = get_data(year, day)
    print(win_bingo(calls, calls_dict, boards))
    print(lose_bingo(calls, calls_dict, boards))


if __name__ == "__main__":
    main()
