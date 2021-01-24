from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    fixed_var = datum[0]
    datum = datum.split(', ')
    fixed_val = int(datum[0][2:])
    other_vals = datum[1][2:].split('..')
    other_vals = [int(val) for val in other_vals]
    return fixed_var, fixed_val, *other_vals


def fill_water(data):
    spring = (500, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    contents = defaultdict(lambda: '.')
    for fixed_var, fixed_val, min_other, max_other in data:
        if fixed_var == 'x':
            x = fixed_val
            for y in range(min_other, max_other + 1):
                contents[x, y] = '#'
        else:
            y = fixed_val
            for x in range(min_other, max_other + 1):
                contents[x, y] = '#'
    shallowest = min(pos[1] for pos in contents)
    deepest = max(pos[1] for pos in contents)
    wet = set()
    water = set()
    first_wet = spring[0] + DOWN[0], spring[1] + DOWN[1]
    assert contents[first_wet] == '.'
    contents[spring] = '+'
    contents[first_wet] = '|'
    wet.add(first_wet)
    updated = True
    while updated:
        updated = False
        wet_to_try = wet.copy()
        counter = 0
        while wet_to_try:
            counter += 1
            if updated:
                break
            x, y = wet_to_try.pop()
            down_coords = x + DOWN[0], y + DOWN[1]
            if down_coords[1] <= deepest:
            # don't care if underwater
                if contents[down_coords] == '.':
                    contents[down_coords] = '|'
                    wet.add(down_coords)
                    updated = True
                elif contents[down_coords] == '|':
                    continue
                else:
                    # think about sideways movement
                    left_blocked = right_blocked = False
                    l_x, l_y = r_x, r_y = x, y
                    left_side = contents[x + LEFT[0], y + LEFT[1]]
                    right_side = contents[x + RIGHT[0], y + RIGHT[1]]
                    if left_side == '|' and right_side == '|':
                        pass
                    elif left_side == '|' and right_side == '#':
                        pass
                    elif left_side == '#' and right_side == '|':
                        pass
                    else:
                        # move wet left
                        while contents[l_x + DOWN[0], l_y + DOWN[1]] in ('~', '#'):
                            l_x, l_y = pos = l_x + LEFT[0], l_y + LEFT[1]
                            if contents[pos] == '#':
                                left_blocked = True
                                break
                            else:
                                contents[pos] = '|'
                                wet.add(pos)
                                updated = True
                        # move wet right
                        while contents[r_x + DOWN[0], r_y + DOWN[1]] in ('~', '#'):
                            r_x, r_y = pos = r_x + RIGHT[0], r_y + RIGHT[1]
                            if contents[pos] == '#':
                                right_blocked = True
                                break
                            else:
                                contents[pos] = '|'
                                wet.add(pos)
                                updated = True
                        # move wet bits and check each side if blocked
                        if left_blocked and right_blocked:
                            # change these to water
                            # middle
                            pos = x, y
                            contents[pos] = '~'
                            wet.remove(pos)
                            water.add(pos)
                            # left
                            l_x, l_y = pos = x + LEFT[0], y + LEFT[1]
                            while contents[pos] == '|':
                                contents[pos] = '~'
                                wet.remove(pos)
                                water.add(pos)
                                updated = True
                                l_x, l_y = pos = l_x + LEFT[0], l_y + LEFT[1]
                            # right
                            r_x, r_y = pos = x + RIGHT[0], y + RIGHT[1]
                            while contents[pos] == '|':
                                contents[pos] = '~'
                                wet.remove(pos)
                                water.add(pos)
                                updated = True
                                r_x, r_y = pos = r_x + RIGHT[0], r_y + RIGHT[1]
    water_count = sum(shallowest <= w[1] <= deepest for w in water)
    wet_count = sum(shallowest <= w[1] <= deepest for w in wet)
    # add spring value if something on level 0
    if shallowest <= 0:
        wet_count += 1
    return water_count + wet_count, water_count


def main():
    year, day = 2018, 17
    data = get_data(year, day)
    reachable, water = fill_water(data)
    print(reachable)
    print(water)


if __name__ == "__main__":
    main()
