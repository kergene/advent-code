from math import ceil
from collections import defaultdict


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = dict(preprocess(datum) for datum in data)
    return data


def preprocess(datum):
    datum = datum.split('=>')
    product = datum[1].strip().split(' ')
    amount = int(product[0])
    product = product[1]
    rest = datum[0].split(',')
    rest = [element.strip().split() for element in rest]
    rest = dict((element[1], int(element[0])) for element in rest)
    return product, (amount, rest)


class Memoize:
    def __init__(self, func):
        self.func = func
        self.memo = {}
    
    def __call__(self, value, data):
        if value not in self.memo:
            self.memo[value] = self.func(value, data)
        return self.memo[value]


@Memoize
def ore_required(element, data):
    if element == 'ORE':
        return 1
    else:
        return sum(ore_required(other_element, data) * needed for other_element, needed in data[element][1].items())


def topological_sort(data):
    elements = dict((element, set(data[element][1])) for element in data)
    sorted_products = []
    while elements:
        products = set(elements)
        requirements = set(element for needed in elements.values() for element in needed)
        to_append = products - requirements
        for next_product in to_append:
            sorted_products.append(next_product)
            del elements[next_product]
    return sorted_products[::-1]


def make_one_fuel(data):
    sorted_elements = topological_sort(data)
    required = defaultdict(int)
    required['FUEL'] = 1
    while sorted_elements:
        choice = sorted_elements.pop()
        needed = required[choice]
        produced = data[choice][0]
        reactions_needed = ceil(needed / produced)
        reaction_inputs = data[choice][1]
        for element, amount in reaction_inputs.items():
            required[element] += amount * reactions_needed
    return required['ORE']


def make_max_fuel(data, ore_needed):
    have = 10 ** 12
    can_make = have // ore_needed
    sorted_elements_fixed = topological_sort(data)
    while True:
        can_make += 1
        sorted_elements = sorted_elements_fixed.copy()
        required = defaultdict(int)
        required['FUEL'] = can_make
        while sorted_elements:
            choice = sorted_elements.pop()
            needed = required[choice]
            produced = data[choice][0]
            reactions_needed = ceil(needed / produced)
            reaction_inputs = data[choice][1]
            for element, amount in reaction_inputs.items():
                required[element] += amount * reactions_needed
        if required['ORE'] > have:
            break
    return can_make - 1


def main():
    year, day = 2019, 14
    data = get_data(year, day)
    ore_needed = make_one_fuel(data)
    print(ore_needed)
    print(make_max_fuel(data, ore_needed))


if __name__ == "__main__":
    main()
