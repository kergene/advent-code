import re
from collections import defaultdict

def get_data(day):
    if day < 10:
        day = '0'+str(day)
    with open(f"input_day_{day}.txt") as f:
        data = f.read().split('\n\n')
    return data

def basic_validation(data):
    ALLOWED_SETS = [{'eyr', 'hgt', 'cid', 'hcl', 'byr', 'iyr', 'pid', 'ecl'},
                    {'eyr', 'hgt', 'hcl', 'byr', 'iyr', 'pid', 'ecl'}]
    data = [set(kv.split(':')[0] for kv in row.split()) in ALLOWED_SETS for row in data]
    return sum(data)

def complex_validation(data):
    data = [{kv.split(':')[0]:kv.split(':')[1] for kv in row.split()} for row in data]
    data = [check_all(fields) for fields in data]
    return sum(data)

def check_all(fields):
    fields = defaultdict(str, fields)
    if not check_year(fields['byr'], 1920, 2002):
        return False
    if not check_year(fields['iyr'], 2010, 2020):
        return False
    if not check_year(fields['eyr'], 2020, 2030):
        return False
    if not ecl_check(fields['ecl']):
        return False
    if not pid_check(fields['pid']):
        return False
    if not hcl_check(fields['hcl']):
        return False
    if not hgt_check(fields['hgt']):
        return False
    return True

def ecl_check(color):
    ALLOWED_COLORS = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
    return color in ALLOWED_COLORS
   
def pid_check(pid):
    match = re.match(r'^[0-9]{9}$', pid)
    return match != None

def hcl_check(hcl):
    match = re.match(r'^#[0-9a-f]{6}$', hcl)
    return match != None

def hgt_check(hgt):
    if hgt[-2:] == 'cm':
        return 150 <= int(hgt[:-2]) <= 193
    elif hgt[-2:] == 'in':
        return 59 <= int(hgt[:-2]) <= 76
    else:
        return False

def check_year(year, min_year, max_year):
    if len(year) == 4:
        return min_year <= int(year) <= max_year
    else:
        return False

def main():
    day = 4
    data = get_data(day)
    n_basic = basic_validation(data)
    print(n_basic)
    n_complex = complex_validation(data)
    print(n_complex)

if __name__ == "__main__":
    main()
