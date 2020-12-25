def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    return data, preprocess(data)


def preprocess(data):
    ALLERGENS = dict()
    for line in data:
        line = line.split('(')
        ingredients = line[0].split()
        recipe_allergens = line[1].split()[1:]
        recipe_allergens = [allergen[:-1] for allergen in recipe_allergens]
        for i in recipe_allergens:
            if i in ALLERGENS:
                ALLERGENS[i].intersection_update(ingredients)
            else:
                ALLERGENS[i] = set(ingredients)
    return ALLERGENS


def safe_ingredients(data, ALLERGENS):
    POTENTIAL_ALLERGEN_INGREDIENTS = set(i for ingredients in ALLERGENS.values() for i in ingredients)
    safe_counter = 0
    for line in data:
        ingredients = line.split('(')[0].split()
        for i in ingredients:
            if i not in POTENTIAL_ALLERGEN_INGREDIENTS:
                safe_counter += 1
    return safe_counter


def cdil(data, ALLERGENS):
    # canonical dangerous ingredient list
    FORCED_ALLERGENS = dict()
    while ALLERGENS:
        for allergen, ingredients in ALLERGENS.items():
            if len(ingredients) == 1:
                choice = ingredients.pop()
                FORCED_ALLERGENS[allergen] = choice
                for other_allergen, other_ingredients in ALLERGENS.items():
                    if choice in other_ingredients:
                        ALLERGENS[other_allergen].remove(choice)
                del ALLERGENS[allergen]
                break
    sorted_keys = sorted(FORCED_ALLERGENS.keys())    
    return ','.join([FORCED_ALLERGENS[key] for key in sorted_keys])


def main():
    year, day = 2020, 21
    data, ALLERGENS = get_data(year, day)
    print(safe_ingredients(data, ALLERGENS))
    print(cdil(data, ALLERGENS))


if __name__ == "__main__":
    main()
