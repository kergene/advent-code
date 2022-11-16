from queue import LifoQueue


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def illegal_syntax(data):
    score = 0
    for row in data:
        stack = LifoQueue()
        for char in row:
            if char in '[({<':
                stack.put(char)
            else:
                if char == ')':
                    if stack.get() != '(':
                        score += 3
                elif char == ']':
                    if stack.get() != '[':
                        score += 57
                elif char == '}':
                    if stack.get() != '{':
                        score += 1197
                elif char == '>':
                    if stack.get() != '<':
                        score += 25137
    return score


def incomplete_lines(data):
    scores = []
    for row in data:
        stack = LifoQueue()
        corrupt = False
        for char in row:
            if char in '[({<':
                stack.put(char)
            else:
                if char == ')':
                    if stack.get() != '(':
                        corrupt = True
                        break
                elif char == ']':
                    if stack.get() != '[':
                        corrupt = True
                        break
                elif char == '}':
                    if stack.get() != '{':
                        corrupt = True
                        break
                elif char == '>':
                    if stack.get() != '<':
                        corrupt = True
                        break
        if not corrupt:
            score = 0
            while stack.qsize() > 0:
                char = stack.get()
                if char == '(':
                    score *= 5
                    score += 1
                elif char == '[':
                    score *= 5
                    score += 2
                elif char == '{':
                    score *= 5
                    score += 3
                elif char == '<':
                    score *= 5
                    score += 4
            scores.append(score)
    scores = sorted(scores)
    return scores [len(scores) // 2]


def main():
    year, day = 2021, 10
    data = get_data(year, day)
    print(illegal_syntax(data))
    print(incomplete_lines(data))


if __name__ == "__main__":
    main()
