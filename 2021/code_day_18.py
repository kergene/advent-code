from math import ceil
from math import floor
from itertools import permutations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return evaluate_snailfish(datum, 1)[0]


def evaluate_snailfish(datum, index):
    snailfish_number = []
    while index < len(datum):
        character = datum[index]
        index += 1
        if character == '[':
            new_snailfish, index = evaluate_snailfish(datum, index)
            snailfish_number.append(new_snailfish)
        elif character == ',':
            pass
        elif character == ']':
            return snailfish_number, index
        else:
            snailfish_number.append(int(character))


class Regular:
    def __init__(self, value, left, right, parent):
        self.value = value
        self.left = left
        if self.left is not None:
            self.left.right = self
        self.right = right
        if self.right is not None:
            self.right.left = self
        self.parent = parent


class Node:
    def __init__(self, left, right, depth, parent, side):
        self.depth = depth
        self.parent = parent
        self.side = side
        if type(left) == list:
            self.left = Node(left[0], left[1], self.depth + 1, self, 'L')
        else:
            self.left = left
        if type(right) == list:
            self.right = Node(right[0], right[1], self.depth + 1, self, 'R')
        else:
            self.right = right

    def Regularize(self, last_reg):
        if type(self.left) == int:
            self.left = Regular(self.left, last_reg, None, self)
            last_reg = self.left
        else:
            last_reg = self.left.Regularize(last_reg)
        if type(self.right) == int:
            self.right = Regular(self.right, last_reg, None, self)
            last_reg = self.right
        else:
            last_reg = self.right.Regularize(last_reg)
        return last_reg

    def add(self, other):
        self.increase_depth()
        other.increase_depth()
        self.side = 'L'
        other.side = 'R'
        new_node = Node(self, other, 0, None, None)
        self.parent = new_node
        other.parent = new_node
        next_right = self.right
        while type(next_right) != Regular:
            next_right = next_right.right
        next_left = other.left
        while type(next_left) != Regular:
            next_left = next_left.left
        next_left.left = next_right
        next_right.right = next_left
        return new_node

    def increase_depth(self):
        self.depth += 1
        if type(self.left) != Regular:
            self.left.increase_depth()
        if type(self.right) != Regular:
            self.right.increase_depth()

    def explode(self):
        if self.depth == 4:
            if self.left.left is not None:
                self.left.left.value += self.left.value
            if self.right.right is not None:
                self.right.right.value += self.right.value
            if self.side == 'L':
                self.parent.left = Regular(0, self.left.left, self.right.right, self.parent)
            elif self.side == 'R':
                self.parent.right = Regular(0, self.left.left, self.right.right, self.parent)
            else:
                assert False
            return True
        else:
            if type(self.left) != Regular:
                try_explode = self.left.explode()
                if try_explode:
                    return True
            if type(self.right) != Regular:
                try_explode = self.right.explode()
                if try_explode:
                    return True
        return False

    def split(self):
        if type(self.left) == Regular:
            if self.left.value >= 10:
                l, r = floor(self.left.value / 2), ceil(self.left.value / 2)
                l_reg = Regular(l, self.left.left, None, self)
                r_reg = Regular(r, l_reg, self.left.right, self)
                self.left = Node(l_reg, r_reg, self.depth + 1, self, 'L')
                return True
        else:
            try_split = self.left.split()
            if try_split:
                return True
        if type(self.right) == Regular:
            if self.right.value >= 10:
                l, r = floor(self.right.value / 2), ceil(self.right.value / 2)
                l_reg = Regular(l, self.right.left, None, self)
                r_reg = Regular(r, l_reg, self.right.right, self)
                self.right = Node(l_reg, r_reg, self.depth + 1, self, 'R')
                return True
        else:
            try_split = self.right.split()
            if try_split:
                return True
        return False

    def magnitude(self):
        if type(self.left) == Regular:
            left_score = self.left.value
        else:
            left_score = self.left.magnitude()
        if type(self.right) == Regular:
            right_score = self.right.value
        else:
            right_score = self.right.magnitude()
        return 3*left_score + 2*right_score


def sum_all(data):
    total = Node(data[0][0], data[0][1], 0, None, None)
    total.Regularize(None)
    for row in data[1:]:
        row_node = Node(row[0], row[1], 0, None, None)
        row_node.Regularize(None)
        total = total.add(row_node)
        while True:
            try_explode = total.explode()
            if not try_explode:
                try_split = total.split()
                if not try_split:
                    break
    return total.magnitude()


def max_sum(data):
    top_score = 0
    for x, y in permutations(data, 2):
        x_node = Node(x[0], x[1], 0, None, None)
        x_node.Regularize(None)
        y_node = Node(y[0], y[1], 0, None, None)
        y_node.Regularize(None)
        total = x_node.add(y_node)
        while True:
            try_explode = total.explode()
            if not try_explode:
                try_split = total.split()
                if not try_split:
                    break
        score = total.magnitude()
        if score > top_score:
            top_score = score
    return top_score


def main():
    year, day = 2021, 18
    data = get_data(year, day)
    print(sum_all(data))
    print(max_sum(data))


if __name__ == "__main__":
    main()
