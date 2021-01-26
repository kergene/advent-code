def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def network(grid):
    DIRECTION = ((1, 0), (0, -1), (0, 1), (-1, 0))
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    dir_idx = 0
    c = grid[0].index('|')
    r = 0
    n_col = len(grid[0])
    n_row = len(grid)
    seen_letters = []
    steps = 0
    while 0 <= r < n_row and 0 <= c < n_col:
        if grid[r][c] in ALPHABET:
            seen_letters.append(grid[r][c])
        elif grid[r][c] == '+':
            for new_idx in range(4):
                if new_idx != 3 - dir_idx:
                    dr, dc = DIRECTION[new_idx]
                    a, b = r + dr, c + dc
                    if grid[a][b] != ' ':
                        dir_idx = new_idx
                        break
        elif grid[r][c] == ' ':
            break
        dr, dc = DIRECTION[dir_idx]
        r, c = r + dr, c + dc
        steps += 1
    return ''.join(seen_letters), steps


def main():
    year, day = 2017, 19
    data = get_data(year, day)
    letters, steps = network(data)
    print(letters)
    print(steps)


if __name__ == "__main__":
    main()
