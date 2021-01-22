def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split()
    data = [int(datum) for datum in data]
    return data


class Tree:
    def __init__(self, parent, child_count, meta_count):
        self.child_count = child_count
        self.meta_count = meta_count
        self.parent = parent
        self.children = []
        self.metadata = []

    def get_value(self):
        if self.children:
            self.value = 0
            for index in self.metadata:
                index -= 1
                if 0 <= index < self.child_count:
                    self.value += self.children[index].value
        else:
            self.value = sum(self.metadata)
        return self.value


def parse_trees(data):
    active_tree = None
    total_metadata = 0
    idx = 0
    while idx < len(data):
        if active_tree == None:
            new_tree = Tree(active_tree, data[idx], data[idx + 1])
            idx += 2
            active_tree = new_tree
        elif len(active_tree.children) < active_tree.child_count:
            new_tree = Tree(active_tree, data[idx], data[idx + 1])
            active_tree.children.append(new_tree)
            idx += 2
            active_tree = new_tree
        else:
            active_tree.metadata = data[idx:idx + active_tree.meta_count]
            total_metadata += sum(active_tree.metadata)
            idx += active_tree.meta_count
            last_tree_value = active_tree.get_value()
            active_tree = active_tree.parent
    return total_metadata, last_tree_value


def main():
    year, day = 2018, 8
    data = get_data(year, day)
    metadata_sum, root_value = parse_trees(data)
    print(metadata_sum)
    print(root_value)


if __name__ == "__main__":
    main()
