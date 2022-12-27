import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import import_data

def get_data(year, day):
    input_path = str(Path(__file__).parent.parent / f"{year}/input_day_{day}.txt")
    with open(input_path) as input_file:
        data = input_file.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum.split()


class CathodeRayTube:
    def __init__(self):
        self.x_value = 1
        self.cycle_number = 0
        self.signal_strengths = 0
        self.picture = []
        self.pixel_row = []
        self.on_pixel = '🟥'
        self.off_pixel  = '⬛' * len(self.on_pixel)

    def noop(self):
        self.cycle_number += 1
        self.check_signal()
        self.draw_pixel()

    def addx(self, val):
        self.noop()
        self.noop()
        self.x_value += val

    def parse(self, input_list):
        if input_list[0] == 'noop':
            self.noop()
        else:
            val = int(input_list[1])
            self.addx(val)

    def check_signal(self):
        if self.cycle_number % 40 == 20:
            self.signal_strengths += self.x_value * self.cycle_number

    @property
    def pixel_number(self):
        return (self.cycle_number - 1) % 40

    @property
    def sprite_locations(self):
        return set(self.x_value + val for val in range(-1, 2))

    def draw_pixel(self):
        if self.pixel_number in self.sprite_locations:
            self.pixel_row.append(self.on_pixel)
        else:
            self.pixel_row.append(self.off_pixel)
        self.update_display()

    def update_display(self):
        if len(self.pixel_row) == 40:
            self.picture.append(self.pixel_row)
            self.pixel_row = []

    def view_crt(self):
        if len(self.pixel_row) > 0:
            self.picture.append(self.pixel_row)
        return '\n'.join(''.join(pixel_row) for pixel_row in self.picture)


def run_crt(data):
    crt = CathodeRayTube()
    for row in data:
        crt.parse(row)
    return crt.signal_strengths, crt.view_crt()


def part_1(data):
    score = 0
    X = 1
    cycle_number = 0
    for row in data:
        inst = row[0]
        if inst == 'noop':
            cycle_number, score = take_step_and_check(cycle_number, score, X)
        else:
            val = int(row[1])
            cycle_number, score = take_step_and_check(cycle_number, score, X)
            cycle_number, score = take_step_and_check(cycle_number, score, X)
            X += val
    return score


def take_step_and_check(cycle_number, score, X):
    cycle_number += 1
    if cycle_number % 40 == 20:
        score += cycle_number * X
    return cycle_number, score


def part_2(data):
    X = 1
    cycle_number = 0
    pixels = []
    for row in data:
        inst = row[0]
        if inst == 'noop':
            cycle_number, to_append = take_step_and_draw(cycle_number, X)
            pixels.append(to_append)
        else:
            val = int(row[1])
            cycle_number, to_append = take_step_and_draw(cycle_number, X)
            pixels.append(to_append)
            cycle_number, to_append = take_step_and_draw(cycle_number, X)
            pixels.append(to_append)
            X += val
    new_pixels = []
    for idx in range(len(pixels) // 40):
        new_pixels.append(pixels[40*idx:40*(idx+1)])
    return '\n'.join(''.join(row) for row in new_pixels)


def take_step_and_draw(cycle_number, X):
    cycle_number += 1
    pixel_pos = cycle_number - 1
    if pixel_pos % 40 in (X-1, X, X+1):
        to_append = '[]'
    else:
        to_append = '  '
    return cycle_number, to_append


def main():
    file_string = str(Path(__file__))
    year, day = import_data.get_year_day(file_string)
    import_data.import_data(year, day)
    data = get_data(year, day)
    signal_strengths, crt_display = run_crt(data)
    print(signal_strengths)
    print(crt_display)


if __name__ == "__main__":
    main()
