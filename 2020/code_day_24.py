from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data


def tile_floor(data):
    flipped = defaultdict(bool)
    for line in data:
        i = 0
        x = y = 0
        while i < len(line):
            if line[i] == 'e':
                x += 2
            elif line[i] == 'w':
                x -= 2
            else:
                if line[i] == 'n':
                    y += 1
                else:
                    y -= 1
                i += 1
                if line[i] == 'e':
                    x += 1
                else:
                    x -= 1
            i += 1
        flipped[(x,y)] = not flipped[(x,y)]
    flipped_tiles = set(i for i in flipped if flipped[i])
    return len(flipped_tiles), flipped_tiles


def take_step(flipped_tiles):
    DIRECTIONS = ((-1,1), (1,1),
                  (-2,0), (2,0),
                  (-1,-1),(1,-1))
    active = defaultdict(int)
    for cell in flipped_tiles:
        x,y = cell
        active[cell] += 1
        for dx, dy in DIRECTIONS:
            neigh = x+dx, y+dy
            active[neigh] += 2
    return set(i for i in active if 3 <= active[i] <= 5)


def living_art(flipped_tiles):
    for _ in range(100):
        flipped_tiles = take_step(flipped_tiles)
    return len(flipped_tiles)


def main():
    year, day = 2020, 24
    data = get_data(year, day)
    tiles_count, flipped_tiles = tile_floor(data)
    print(tiles_count)
    print(living_art(flipped_tiles))


if __name__ == "__main__":
    main()
