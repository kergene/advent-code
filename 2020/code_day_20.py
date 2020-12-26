from math import prod
from collections import Counter
from itertools import product, combinations


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    # dictionary with tile_id: image
    data = dict(preprocess(datum) for datum in data)
    return data


def preprocess(datum):
    datum = datum.splitlines()
    tile_id = int(datum[0].split()[1][:-1])
    rest = datum[1:]
    return tile_id, rest


def get_sides(tile_id, data):
    # returns set of sides of tile
    sides = set()
    tile = data[tile_id]
    sides.add(tile[0])
    sides.add(tile[0][::-1])
    sides.add(tile[-1])
    sides.add(tile[-1][::-1])
    left = ''.join(row[0] for row in tile)
    right = ''.join(row[-1] for row in tile)
    sides.add(left)
    sides.add(left[::-1])
    sides.add(right)
    sides.add(right[::-1])
    return sides


def find_corners(data):
    # part 1: returns product of corners
    edges = set()
    for tile1, tile2 in combinations(data.keys(), 2):
        sides1 = get_sides(tile1, data)
        sides2 = get_sides(tile2, data)
        if sides1.intersection(sides2):
            edges.add((tile1, tile2))
            edges.add((tile2, tile1))
    firsts = [edge[0] for edge in edges]
    return prod(i[0] for i in Counter(firsts).most_common()[-4:]), edges


def neighbours(tile_id, edges):
    # returns neighbours of a cell from edge list
    return [edge[1] for edge in edges if edge[0] == tile_id]


def construct_grid(edges):
    # constructs grid of numbers (not needed for part 1)
    grid = [[0 for _ in range(12)] for _ in range(12)]
    # pick and set top right cell
    firsts = [edge[0] for edge in edges]
    appears = Counter(firsts).most_common()
    grid[0][0] = appears[-1][0]
    # pick and set (1,0) and (0,1)
    neigbours00 = neighbours(grid[0][0], edges)
    grid[1][0] = neigbours00[0]
    grid[0][1] = neigbours00[1]
    # set (i, 0) for each i
    for i in range(2, 12):
        last = grid[i-1][0]
        neighbours_last = neighbours(last, edges)
        for neighbour in neighbours_last:
            if neighbour != grid[i-2][0]:
                if len(neighbours(neighbour, edges)) < 4:
                    grid[i][0] = neighbour
                    break
    # set (0, j) for each j
    for j in range(2, 12):
        last = grid[0][j-1]
        neighbours_last = neighbours(last, edges)
        for neighbour in neighbours_last:
            if neighbour != grid[0][j-2]:
                if len(neighbours(neighbour, edges)) < 4:
                    grid[0][j] = neighbour
                    break
    # use cells above and left of a cell to set rest of grid
    for i, j in product(range(1,12), repeat=2):
        left = grid[i-1][j]
        above = grid[i][j-1]
        used_id = grid[i-1][j-1]
        neighbours_left = neighbours(left, edges)
        neighbours_above = neighbours(above, edges)
        for neighbour in neighbours_left:
            if neighbour != used_id:
                if neighbour in neighbours_above:
                    grid[i][j] = neighbour
    return grid


def rotate_anti(tile_id, data):
    # rotates tile 90 degrees anticlockwise
    grid = data[tile_id]
    new_grid = [['' for _ in range(10)] for _ in range(10)]
    for i, j in product(range(10), repeat=2):
        new_grid[i][j] = grid[j][9-i]
    data[tile_id] = [''.join(row) for row in new_grid]


def flip(tile_id, data):
    # flips tile
    data[tile_id] = [''.join(row) for row in zip(*data[tile_id])]


def construct_image(data, edges):
    # reconstruct image from mess of subimages
    grid = construct_grid(edges)
    image_grid = [['' for _ in range(12)] for _ in range(12)]
    # transform top left image until could match (1,0) and (0,1)
    left_edges = get_sides(grid[0][1], data)
    top_edges = get_sides(grid[1][0], data)
    tile_id = grid[0][0]
    rotates = 0
    while rotates < 4:
        right = ''.join(row[-1] for row in data[tile_id])
        if right in left_edges:
            break
        else:
            rotate_anti(tile_id, data)
            rotates += 1
    bottom = data[tile_id][-1]
    if bottom not in top_edges:
        flip(tile_id, data)
        rotates = 0
        while rotates < 4:
            left = ''.join(row[0] for row in data[tile_id])
            if right in left_edges:
                break
            else:
                rotate_anti(tile_id, data)
                rotates += 1
    image_grid[0][0] = data[tile_id]
    # fill in images in first row (working across)
    #     transform until we find a fit
    for j in range(1, 12):
        tile_id = grid[0][j]
        right = ''.join(row[-1] for row in image_grid[0][j-1])
        rotates = 0
        while rotates < 4:
            left = ''.join(row[0] for row in data[tile_id])
            if right == left:
                break
            else:
                rotate_anti(tile_id, data)
                rotates += 1
        if right != left:
            flip(tile_id, data)
            rotates = 0
            while rotates < 4:
                left = ''.join(row[0] for row in data[tile_id])
                if right == left:
                    break
                else:
                    rotate_anti(tile_id, data)
                    rotates += 1
        image_grid[0][j] = data[tile_id]
    # fill in rest of images (working down)
    #     transform until we find a fit
    for i, j in product(range(1, 12), range(0, 12)):
        tile_id = grid[i][j]
        bottom = image_grid[i-1][j][-1]
        rotates = 0
        while rotates < 4:
            top = data[tile_id][0]
            if bottom == top:
                break
            else:
                rotate_anti(tile_id, data)
                rotates += 1
        if bottom != top:
            flip(tile_id, data)
            rotates = 0
            while rotates < 4:
                top = data[tile_id][0]
                if bottom == top:
                    break
                else:
                    rotate_anti(tile_id, data)
                    rotates += 1
        image_grid[i][j] = data[tile_id]
    # trim borders of subimages
    for i, j in product(range(0, 12), repeat=2):
        image_grid[i][j] = [row[1:-1] for row in image_grid[i][j][1:-1]]
    # convert subimages to one image
    image = []
    for image_grid_row in range(0,12):
        for subimage_row in range(0,8):
            image_row = [subimage[subimage_row] for subimage in image_grid[image_grid_row]]
            image.append(''.join(image_row))
    return image


def rotate_anti_image(image):
    # rotate image anticlockwise by 90 deg
    new_image = [['' for _ in range(96)] for _ in range(96)]
    for i, j in product(range(96), repeat=2):
        new_image[i][j] = image[j][95-i]
    return [''.join(row) for row in new_image]


def flip_image(image):
    # flip whole image
    return [''.join(row) for row in zip(*image)]


def count_seamonsters(seamonster, image):
    # counts seamonsters in image
    # for each possible top left cell
    #     check if all rows match
    # 3 x 20 seamonster
    # 96 x 96 image
    n = 0
    for i, j in product(range(96 - 2), range(96 - 19)):
        row = image[i][j:j+20]
        if all(row[dark] == '#' for dark in seamonster[0]):
            row = image[i+1][j:j+20]
            if all(row[dark] == '#' for dark in seamonster[1]):
                row = image[i+2][j:j+20]
                if all(row[dark] == '#' for dark in seamonster[2]):
                    n += 1
    return n


def find_seamonsters(data, edges):
    # returns number of non-seamonster dark squares
    seamonster = [
        [18],
        [0, 5, 6, 11, 12, 17, 18, 19],
        [1, 4, 7, 10, 13, 16]
    ]
    image = construct_image(data, edges)
    # transform until we find a seamonster
    rotate = 0
    while rotate < 4:
        n = count_seamonsters(seamonster, image)
        if n:
            break
        else:
            rotate += 1
            image = rotate_anti_image(image)
    if n:
        pass
    else:
        image = flip_image(image)
        rotate = 0
        while rotate < 4:
            n = count_seamonsters(seamonster, image)
            if n:
                break
            else:
                rotate += 1
                image = rotate_anti_image(image)
    dark_count = sum(pixel == '#' for row in image for pixel in row)
    return dark_count - n*15


def main():
    year, day = 2020, 20
    data = get_data(year, day)
    ans, edges = find_corners(data)
    print(ans)
    print(find_seamonsters(data, edges))


if __name__ == "__main__":
    main()
