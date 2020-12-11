DIRECTIONS = ((-1,-1),(-1,0),(-1,1),
              (0,-1),        (0,1),
              (1,-1), (1,0), (1,1))

def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [[element  for element in row] for row in data]
    return data

def test_equality(data, new_data):
    for i in range(len(new_data)):
        if new_data[i] != data[i]:
            return False
    return True

def find_stability(data):
    stable = False
    while not stable:
        new_data = take_step(data)
        stable = test_equality(data, new_data)
        data = new_data
    return sum(1 for row in data for element in row if element == '#')

def take_step(data):
    new_data = [row.copy() for row in data]
    for x in range(len(data)):
        for y in range(len(data[0])):
            fulls = 0
            for dx, dy in DIRECTIONS:
                a,b = x+dx,y+dy
                if 0 <= a < len(data) and 0 <= b < len(data[0]):
                    if data[a][b] == '#':
                        fulls += 1
            if data[x][y] == 'L' and fulls == 0:
                new_data[x][y] = '#'
            elif data[x][y] == '#' and fulls >= 4:
                new_data[x][y] = 'L'
    return new_data

def find_stability_long_see(data):
    stable = False
    while not stable:
        new_data = take_step_long_see(data)
        stable = test_equality(data, new_data)
        data = new_data
    return sum(1 for row in data for element in row if element == '#')

def take_step_long_see(data):
    new_data = [row.copy() for row in data]
    for x in range(len(data)):
        for y in range(len(data[0])):
            fulls = 0
            for dx, dy in DIRECTIONS:
                a,b=x,y
                seat = False
                while not seat:
                    a,b = a+dx,b+dy
                    seat = True
                    if 0<= a < len(data) and 0 <= b < len(data[0]):
                        if data[a][b] == '.':
                            seat = False
                        elif data[a][b] == '#':
                            fulls += 1
            if data[x][y] == 'L' and fulls == 0:
                new_data[x][y] = '#'
            elif data[x][y] == '#' and fulls >= 5:
                new_data[x][y] = 'L'
    return new_data

def main():
    day = 11
    data = get_data(day)
    print(find_stability(data))
    print(find_stability_long_see(data))

if __name__ == "__main__":
    main()
