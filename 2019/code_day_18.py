from itertools import product
from heapdict import heapdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return list(datum)


def get_start_distances(grid):
    n_rows = len(grid)
    n_cols = len(grid[0])
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    DIRECTIONS = ((1,0), (-1, 0), (0, 1), (0, -1))
    NON_WALLS = ALPHABET + alphabet +  '.' + '@'
    letters = dict()
    for r, c in product(range(n_rows), range(n_cols)):
        if grid[r][c] == '@':
            vault_start = r, c
        elif grid[r][c] in alphabet:
            letters[grid[r][c]] = r, c
    start = vault_start
    q = set()
    q.add(start)
    distances = dict()
    distances[start] = 0
    seen_alphabets = dict()
    seen_alphabets[start] = set()
    while q:
        r, c = choice = min(q, key=distances.get)
        q.remove(choice)
        distance = distances[choice]
        current_hits = seen_alphabets[choice]
        for dr, dc in DIRECTIONS:
            a, b = pos = r + dr, c + dc
            pos_state = grid[a][b]
            if pos_state in NON_WALLS:
                if pos in distances:
                    if distances[pos] > distance + 1:
                        distances[pos] = distance + 1
                        seen_alphabets[pos] = current_hits + pos_state
                        q.add(pos)
                else:
                    distances[pos] = distance + 1
                    seen_alphabets[pos] = current_hits | set(pos_state)
                    q.add(pos)
    return distances, seen_alphabets, letters


def produce_distances(grid):
    distances, seen_alphabets, letters = get_start_distances(grid)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    DIRECTIONS = ((1,0), (-1, 0), (0, 1), (0, -1))
    NON_WALLS = ALPHABET + alphabet +  '.' + '@'
    NON_BLOCKERS = set('.@')
    blockers = dict()
    main_distances = dict()
    for letter, location in letters.items():
        blockers[ord(letter) - 97] = set(ord(thing.upper()) - 65 for thing in seen_alphabets[location] - NON_BLOCKERS) - set((ord(letter) - 97,))
        main_distances[ord('@') - 65, ord(letter) - 97] = distances[location]
        start = location
        q = set()
        q.add(start)
        other_distances = dict()
        other_distances[start] = 0
        while q:
            r, c = choice = min(q, key=other_distances.get)
            q.remove(choice)
            distance = other_distances[choice]
            for dr, dc in DIRECTIONS:
                a, b = pos = r + dr, c + dc
                if grid[a][b] in NON_WALLS:
                    if pos in other_distances:
                        if other_distances[pos] > distance + 1:
                            other_distances[pos] = distance + 1
                            q.add(pos)
                    else:
                        other_distances[pos] = distance + 1
                        q.add(pos)
        for other_letter, other_location in letters.items():
            main_distances[ord(letter) - 97, ord(other_letter) - 97] = other_distances[other_location]
    n_letters = len(letters)
    return n_letters, blockers, main_distances


def key_collection(grid):
    n_letters, blockers, main_distances = produce_distances(grid)
    start = tuple([-1] + [0] * n_letters)
    distances = heapdict()
    distances[start] = 0
    seens = set()
    while distances:
        choice, distance = distances.popitem()
        current, *visited = choice
        seens.add(choice)
        if all(visited):
            return distance
        for next_letter in range(n_letters):
            # if unvisited
            if not visited[next_letter]:
                if all(visited[blocker] for blocker in blockers[next_letter]):
                    new_visited = list(visited)
                    new_visited[next_letter] = 1
                    new_choice = tuple([next_letter] + new_visited)
                    if new_choice not in seens:
                        new_distance = distance + main_distances[current, next_letter]
                        if new_choice in distances:
                            if new_distance < distances[new_choice]:
                                distances[new_choice] = new_distance
                        else:
                            distances[new_choice] = new_distance
    assert False


def change_grid(grid):
    n_rows = len(grid)
    n_cols = len(grid[0])
    for r, c in product(range(n_rows), range(n_cols)):
        if grid[r][c] == '@':
            start = [r, c]
            break
    r, c = start
    grid[r][c] = '#'
    grid[r + 1][c] = '#'
    grid[r - 1][c] = '#'
    grid[r][c + 1] = '#'
    grid[r][c - 1] = '#'
    grid[r + 1][c + 1] = '@'
    grid[r + 1][c - 1] = '@'
    grid[r - 1][c + 1] = '@'
    grid[r - 1][c - 1] = '@'
    return grid


def get_quad_start_distances(grid):
    n_rows = len(grid)
    n_cols = len(grid[0])
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    DIAGONALS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
    DIRECTIONS = ((1,0), (-1, 0), (0, 1), (0, -1))
    NON_WALLS = ALPHABET + alphabet +  '.' + '@'
    NON_BLOCKERS = set('.@')
    letters = dict()
    for r, c in product(range(n_rows), range(n_cols)):
        if grid[r][c] == '@':
            vault_start = r, c
        elif grid[r][c] in alphabet:
            letters[grid[r][c]] = r, c
    blockers = dict()
    main_distances = dict()
    grid = change_grid(grid)
    for idx, dpos in enumerate(DIAGONALS):
        dr, dc = dpos
        r, c = vault_start
        start = r + dr, c + dc
        q = set()
        q.add(start)
        distances = dict()
        distances[start] = 0
        seen_alphabets = dict()
        seen_alphabets[start] = set()
        while q:
            r, c = choice = min(q, key=distances.get)
            q.remove(choice)
            distance = distances[choice]
            current_hits = seen_alphabets[choice]
            for dr, dc in DIRECTIONS:
                a, b = pos = r + dr, c + dc
                pos_state = grid[a][b]
                if pos_state in NON_WALLS:
                    if pos in distances:
                        if distances[pos] > distance + 1:
                            distances[pos] = distance + 1
                            seen_alphabets[pos] = current_hits + pos_state
                            q.add(pos)
                    else:
                        distances[pos] = distance + 1
                        seen_alphabets[pos] = current_hits | set(pos_state)
                        q.add(pos)
        for letter, location in letters.items():
            if location in seen_alphabets:
                blockers[ord(letter) - 97] = set(ord(thing.upper()) - 65 for thing in seen_alphabets[location] - NON_BLOCKERS) - set((ord(letter) - 97, ))
                main_distances[ord('@') - 65 - idx, ord(letter) - 97] = distances[location]
    return main_distances, blockers, letters, grid


def produce_quad_distances(grid):
    # distances/blockers are same as before, except:
    # 1. distance from @ -> letter reduces by 2
    # 2. distances only exist for letters in same quadrant
    # 3. need to separate initial distances by quadrants
    main_distances, blockers, letters, grid = get_quad_start_distances(grid)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    DIRECTIONS = ((1,0), (-1, 0), (0, 1), (0, -1))
    NON_WALLS = ALPHABET + alphabet +  '.' + '@'
    for letter, location in letters.items():
        start = location
        q = set()
        q.add(start)
        other_distances = dict()
        other_distances[start] = 0
        while q:
            r, c = choice = min(q, key=other_distances.get)
            q.remove(choice)
            distance = other_distances[choice]
            for dr, dc in DIRECTIONS:
                a, b = pos = r + dr, c + dc
                if grid[a][b] in NON_WALLS:
                    if pos in other_distances:
                        if other_distances[pos] > distance + 1:
                            other_distances[pos] = distance + 1
                            q.add(pos)
                    else:
                        other_distances[pos] = distance + 1
                        q.add(pos)
        for other_letter, other_location in letters.items():
            if other_location in other_distances:
                main_distances[ord(letter) - 97, ord(other_letter) - 97] = other_distances[other_location]
    n_letters = len(letters)
    return n_letters, blockers, main_distances


def quad_key_collection(grid):
    n_letters, blockers, main_distances = produce_quad_distances(grid)
    start = tuple([-1, -2, -3, -4] + [0] * n_letters)
    distances = heapdict()
    distances[start] = 0
    seens = set()
    while distances:
        choice, distance = distances.popitem()
        c1, c2, c3, c4, *visited = choice
        current = [c1, c2, c3, c4]
        seens.add(choice)
        if all(visited):
            return distance
        for next_letter in range(n_letters):
            # if unvisited
            if not visited[next_letter]:
                if all(visited[blocker] for blocker in blockers[next_letter]):
                    for idx, letter in enumerate(current):
                        # true for exactly one letter
                        if (letter, next_letter) in main_distances:
                            current_copy = current.copy()
                            current_copy[idx] = next_letter
                            new_visited = list(visited)
                            new_visited[next_letter] = 1
                            new_choice = tuple(current_copy + new_visited)
                            if new_choice not in seens:
                                new_distance = distance + main_distances[letter, next_letter]
                                if new_choice in distances:
                                    if new_distance < distances[new_choice]:
                                        distances[new_choice] = new_distance
                                else:
                                    distances[new_choice] = new_distance
                            break
    assert False


def main():
    year, day = 2019, 18
    data = get_data(year, day)
    print(key_collection(data))
    print(quad_key_collection(data))


if __name__ == "__main__":
    main()
