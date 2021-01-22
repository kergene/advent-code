def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [list(datum) for datum in data]
    return data


class Cart:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.junction_index = 0

    def take_step(self, grid):
        self.x += self.dx
        self.y += self.dy
        tile = grid[self.y][self.x]
        if tile == '/':
            if self.dx == 1:
                self.dx = 0
                self.dy = -1
            elif self.dx == -1:
                self.dx = 0
                self.dy = 1
            elif self.dy == 1:
                self.dx = -1
                self.dy = 0
            elif self.dy == -1:
                self.dx = 1
                self.dy = 0
        elif tile == '\\':
            if self.dx == 1:
                self.dx = 0
                self.dy = 1
            elif self.dx == -1:
                self.dx = 0
                self.dy = -1
            elif self.dy == 1:
                self.dx = 1
                self.dy = 0
            elif self.dy == -1:
                self.dx = -1
                self.dy = 0
        elif tile == '+':
            if self.dx == 1:
                if self.junction_index == 0:
                    self.junction_index = 1
                    self.dx = 0
                    self.dy = -1
                elif self.junction_index == 1:
                    self.junction_index = 2
                elif self.junction_index == 2:
                    self.junction_index = 0
                    self.dx = 0
                    self.dy = 1
            elif self.dx == -1:
                if self.junction_index == 0:
                    self.junction_index = 1
                    self.dx = 0
                    self.dy = 1
                elif self.junction_index == 1:
                    self.junction_index = 2
                elif self.junction_index == 2:
                    self.junction_index = 0
                    self.dx = 0
                    self.dy = -1
            elif self.dy == 1:
                if self.junction_index == 0:
                    self.junction_index = 1
                    self.dx = 1
                    self.dy = 0
                elif self.junction_index == 1:
                    self.junction_index = 2
                elif self.junction_index == 2:
                    self.junction_index = 0
                    self.dx = -1
                    self.dy = 0
            elif self.dy == -1:
                if self.junction_index == 0:
                    self.junction_index = 1
                    self.dx = -1
                    self.dy = 0
                elif self.junction_index == 1:
                    self.junction_index = 2
                elif self.junction_index == 2:
                    self.junction_index = 0
                    self.dx = 1
                    self.dy = 0
    
    def check_collision(self, other):
        return self.x == other.x and self.y == other.y


def find_crash(grid):
    grid = [row.copy() for row in grid]
    vehicles = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            tile = grid[y][x]
            if tile == 'v':
                vehicles.append(Cart(x, y, 0, 1))
                grid[y][x] = '|'
            elif tile == '^':
                vehicles.append(Cart(x, y, 0, -1))
                grid[y][x] = '|'
            elif tile == '<':
                vehicles.append(Cart(x, y, -1, 0))
                grid[y][x] = '-'
            elif tile == '>':
                vehicles.append(Cart(x, y, 1, 0))
                grid[y][x] = '-'
    while True:
        vehicles = sorted(vehicles, key=lambda cart: (cart.x, cart.y))
        for idx in range(len(vehicles)):
            cart = vehicles[idx]
            cart.take_step(grid)
            for other in range(len(vehicles)):
                if other != idx:
                    if cart.check_collision(vehicles[other]):
                        return str(cart.x) + ',' + str(cart.y)


def last_cart(grid):
    vehicles = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            tile = grid[y][x]
            if tile == 'v':
                vehicles.append(Cart(x, y, 0, 1))
                grid[y][x] = '|'
            elif tile == '^':
                vehicles.append(Cart(x, y, 0, -1))
                grid[y][x] = '|'
            elif tile == '<':
                vehicles.append(Cart(x, y, -1, 0))
                grid[y][x] = '-'
            elif tile == '>':
                vehicles.append(Cart(x, y, 1, 0))
                grid[y][x] = '-'
    while len(vehicles) > 1:
        vehicles = sorted(vehicles, key=lambda cart: (cart.x, cart.y))
        for idx in range(len(vehicles)):
            cart = vehicles[idx]
            if cart is not None:
                cart.take_step(grid)
                for other in range(len(vehicles)):
                    if other != idx:
                        other_cart = vehicles[other]
                        if other_cart is not None:
                            if cart.check_collision(other_cart):
                                vehicles[idx] = None
                                vehicles[other] = None
                                break
        vehicles = [cart for cart in vehicles if cart is not None]
    last = vehicles[0]
    return str(last.x) + ',' + str(last.y)


def main():
    year, day = 2018, 13
    data = get_data(year, day)
    print(find_crash(data))
    print(last_cart(data))


if __name__ == "__main__":
    main()
