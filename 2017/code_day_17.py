def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return int(data)


def spinlock(data):
    loop = LinkedLoop(data)
    loop.add(0)
    for idx in range(1, 2018):
        loop.step()
        loop.add(idx)
    return loop.focus.next.value


class LinkedNode:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node
    

class LinkedLoop:
    def __init__(self, steps):
        self.focus = None
        self.steps = steps
    
    def add(self, value):
        if self.focus == None:
            self.focus = LinkedNode(value)
            self.focus.next = self.focus
        else:
            self.focus.next = LinkedNode(value, self.focus.next)
            self.focus = self.focus.next
    
    def step(self):
        for _ in range(self.steps):
            self.focus = self.focus.next


def super_spinlock(data):
    focus_idx = 0
    length = 1
    for val in range(1, 5 * 10**7 + 1):
        focus_idx += data
        focus_idx %= length
        if focus_idx == 0:
            final_zero = val
        length += 1
        focus_idx += 1
    return final_zero


def main():
    year, day = 2017, 17
    data = get_data(year, day)
    print(spinlock(data))
    print(super_spinlock(data))


if __name__ == "__main__":
    main()
