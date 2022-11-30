import os
from pathlib import Path
import requests

YEARS = tuple(str(year_ex) for year_ex in range(2015, 2023))
DAYS = tuple(['0'+str(day_ex) for day_ex in range(1,10)] + [str(day_ex) for day_ex in range(10, 26)])

def import_data(year, day):
    input_path = str(Path(__file__).parent / f"{year}/input_day_{day}.txt")
    print(input_path)
    if os.path.isfile(input_path):
        pass
    else:
        if year not in YEARS:
            raise ValueError('Invalid year input')
        if day not in DAYS:
            raise ValueError('Invalid day input')
        input_text = get_input(year, day)
        with open(input_path, "w") as input_file:
            input_file.write(input_text)


def get_input(year, day):
    with open(str(Path(__file__).parent / ".aocrc")) as cookie_file:
        aoc_cookie = cookie_file.read().strip()
    req = requests.get(f'https://adventofcode.com/{year}/day/{int(day)}/input',
                       headers={'cookie':'session='+aoc_cookie})
    return req.text


def get_year_day(file_string):
    directories = file_string.split('/')
    year = directories[-2]
    day = directories[-1][-5:-3]
    return year, day


if __name__ == '__main__':
    get_year_day('/Users/kerem/coding_projects/personal/python/advent_of_code/2022/code_day_01.py')
