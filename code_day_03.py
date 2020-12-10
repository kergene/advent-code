from math import prod

def get_data():
    with open("input_day_3.txt") as f:
        data = f.read()
    data = data.splitlines()
    return data

def count_trees(data, right, down):
    trees = 0
    col = 0
    col_length = len(data[0])
    for row in range(0, len(data), down):
        if data[row][col] == '#':
             trees += 1
        col += right
        col = col % col_length
    return trees

if __name__ == "__main__":
    data = get_data()
    tree_list = []
    steps = ((1,1), (3,1), (5,1), (7,1), (1,2))
    for right, down in steps:
        tree_list.append(count_trees(data, right, down))
    print(tree_list[1])
    print(prod(tree_list))