def get_data():
    with open("input_day_6.txt") as f:
        data = f.read().split('\n\n')
    return data

def count_anyone(data):
    return sum(len(set(''.join(group.splitlines()))) for group in data)

def count_everyone(data):
    total = 0
    for group in data:
        everyone = set('acbdefghijklmnopqrstuvwxyz')
        for person in group.splitlines():
            everyone.intersection_update(set(person))
        total += len(everyone)
    return total    

if __name__ == "__main__":
    data = get_data()
    print(count_anyone(data))
    print(count_everyone(data))