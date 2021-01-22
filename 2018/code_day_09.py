def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    data = [int(datum) for datum in preprocess(data)]
    return data


def preprocess(datum):
    datum = datum.split()
    return datum[0], datum[-2]


class DoublyLinkedLoopNode(object):
    def __init__(self, value):
        self.value =  value
        self.prev = None
        self.next = None
    
    def __str__(self):
        return str(self.value)


class DoublyLinkedLoop(object):
    def __init__(self):
        self.focus = None

    def add(self, value):
        node = DoublyLinkedLoopNode(value)
        if not self.focus:
            self.focus = node
            self.focus.prev = node
            self.focus.next = node
            return node
        else:
            self.focus.next.prev = node
            node.prev = self.focus
            node.next = self.focus.next
            self.focus.next = node
            self.focus = self.focus.next
            return node

    def __str__(self):
        initial = self.focus.value
        cur = self.focus.next
        vals = [initial]
        while cur.value != initial:
            vals.append(cur.value)
            cur = cur.next
        return str(vals)

    def pop(self):
        # assume has sufficiently many elements
        popped = self.focus
        self.focus = popped.next
        self.focus.prev = popped.prev
        popped.prev.next = self.focus
        return popped

    def advance_focus(self):
        self.focus = self.focus.next
    
    def move_back_seven(self):
        self.focus = self.focus.prev.prev.prev.prev.prev.prev.prev


def run_game(n_elves, max_marble):
    elf_scores = [0] * n_elves
    elf = 0
    dll = DoublyLinkedLoop()
    dll.add(0)
    for idx in range(1, max_marble + 1):
        if idx % 23:
            dll.advance_focus()
            dll.add(idx)
        else:
            #score
            elf_scores[elf] += idx
            dll.move_back_seven()
            new_score = dll.pop()
            elf_scores[elf] += new_score.value
        elf += 1
        elf %= n_elves
    return max(elf_scores)


def marble_score(data):
    n_elves = data[0]
    max_marble = data[1]
    return run_game(n_elves, max_marble)


def marble_score_big(data):
    n_elves = data[0]
    max_marble = data[1] * 100
    return run_game(n_elves, max_marble)


def main():
    year, day = 2018, 9
    data = get_data(year, day)
    print(marble_score(data))
    print(marble_score_big(data))


if __name__ == "__main__":
    main()
