import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import import_data


class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = {}
        self.subfiles = {}
    
    def get_size(self):
        file_sum = sum(subfile.size for subfile in self.subfiles.values())
        dir_sum = sum(child.get_size() for child in self.children.values())
        return file_sum + dir_sum
    
    def get_small_sum(self):
        dir_sum = self.get_size()
        dir_small_sum = sum(child.get_small_sum() for child in self.children.values())
        if dir_sum <= 100000:
            return dir_sum + dir_small_sum
        return dir_small_sum
    
    def find_min(self, size_to_delete):
        min_val = 70000000
        if self.get_size() >= size_to_delete:
            min_val = self.get_size()
            sub_min = min(child.find_min(size_to_delete) for child in self.children.values())
            min_val = min(sub_min, min_val)
        return min_val


class File:
    def __init__(self, name, parent, size):
        self.name = name
        self.parent = parent
        self.size = size


def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    return create_file_structure(data)


def create_file_structure(data):
    root = Directory('/', None)
    current_directory = root
    row_idx = 0
    while row_idx < len(data):
        row = data[row_idx].split()
        if row[0] == '$':
            if row[1] == 'cd':
                # move directory
                if row[2] == '/':
                    current_directory = root
                elif row[2] == '..':
                    assert current_directory.parent is not None
                    current_directory = current_directory.parent
                else:
                    # check we've run ls first
                    assert row[2] in current_directory.children
                    current_directory = current_directory.children[row[2]]
            else:
                # check we don't add files twice
                assert len(current_directory.children) == 0
                assert len(current_directory.subfiles) == 0
        else:
            if row[0] == 'dir':
                new = Directory(row[1], current_directory)
                current_directory.children[row[1]] = new
            else:
                new = File(row[1], current_directory, int(row[0]))
                current_directory.subfiles[row[1]] = new
        row_idx += 1
    return root


def sum_small_directories(root):
    return root.get_small_sum()


def find_deletion(root):
    total_size = 70000000
    size_needed = 30000000
    size_remaining = total_size - root.get_size()
    size_to_delete = size_needed - size_remaining
    return root.find_min(size_to_delete)


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    print(sum_small_directories(data))
    print(find_deletion(data))


if __name__ == "__main__":
    main()
