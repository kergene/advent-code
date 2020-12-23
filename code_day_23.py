def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read()
    return [int(i) for i in data]


class DoublyLinkedListNode(object):
    def __init__(self, value):
        self.value =  value
        self.prev = None
        self.next = None


class DoublyLinkedList(object):
    def __init__(self):
        self.focus = None

    def add(self, value):
        node = DoublyLinkedListNode(value)
        if not self.focus:
            self.focus = node
            self.focus.prev = node
            self.focus.next = node
            return node
        else:
            self.focus.prev.next = node
            node.prev = self.focus.prev
            node.next = self.focus
            self.focus.prev = node
            return node

    def __str__(self):
        initial = self.focus.value
        cur = self.focus.next
        vals = [initial]
        while cur.value != initial:
            vals.append(cur.value)
            cur = cur.next
        return(str(vals))

    def pop_triple(self):
        # assume has sufficiently many elements
        popped = self.focus
        self.focus = popped.next.next.next
        self.focus.prev = popped.prev
        self.focus.prev.next = self.focus
        return popped

    def advance_focus(self):
        self.focus = self.focus.next
        return self.focus.prev

    def insert_after_triple(self, after_node, first, second, third):
        third = first.next.next
        before_node = after_node.next
        after_node.next = first
        first.prev = after_node
        before_node.prev = third
        third.next = before_node


class CupGame(object):
    def __init__(self, iterator):
        self.value_to_node = {}
        self.dll = DoublyLinkedList()
        for value in iterator:
            node = self.dll.add(value)
            self.value_to_node[value] = node

    def next_value(self, current_value):
        destination_value = current_value - 1
        if destination_value == 0:
            destination_value = self.max
        return destination_value

    def take_step(self):
        current = self.dll.advance_focus()
        first = self.dll.pop_triple()
        second, third = first.next, first.next.next
        removed_values = (first.value, second.value, third.value)
        destination_value = self.next_value(current.value)
        while destination_value in removed_values:
            destination_value = self.next_value(destination_value)
        destination = self.value_to_node[destination_value]
        self.dll.insert_after_triple(destination, first, second, third)

    def score(self):
        one = self.value_to_node[1]
        first = one.next
        second = first.next
        return first.value * second.value

    def unravel(self):
        current_node = self.value_to_node[1].next
        nodes_visited = []
        while current_node.value != 1:
            nodes_visited.append(current_node.value)
            current_node = current_node.next
        return ''.join(str(value) for value in nodes_visited)

    @property
    def max(self):
        return max(self.value_to_node)


def find_ordering(data):
    cups = CupGame(data)
    for _ in range(100):
        cups.take_step()
    return cups.unravel()


def data_generator(data, max_value):
    i = 0
    for value in data:
        i += 1
        yield value
    while i < max_value:
        i += 1
        yield i


def find_stars(data):
    cups = CupGame(data_generator(data, 1000000))
    for _ in range(10000000):
        cups.take_step()
    return cups.score()


def main():
    day = 23
    data = get_data(day)
    print(find_ordering(data))
    print(find_stars(data))


if __name__ == "__main__":
    main()
