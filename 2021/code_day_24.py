def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().splitlines()
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return datum.split()


def find_model_numbers(data):
    stack = []
    conditions = []
    subdata_length = len(data) // 14    
    for idx in range(14):
        subdata = data[idx*subdata_length:(idx + 1)*subdata_length]
        if subdata[4][2] == '1':
            stack.append((idx, int(subdata[15][2])))
        else:
            old_idx, old_val = stack.pop()
            new_val = int(subdata[5][2])
            conditions.append((old_idx, old_val + new_val, idx))
    low = [0]*14
    high = [0]*14
    # conditions are of the form i[primary] + value = i[secondary]
    for primary, value, secondary in conditions:
        if secondary > primary:
            primary, secondary = secondary, primary
            value *= -1
            if value > 0:
                high[primary] = 9 - value
                high[secondary] = 9
                low[primary] = 1
                low[secondary] = 1 + value
            else:
                high[primary] = 9
                high[secondary] = 9 + value
                low[primary] = 1 - value
                low[secondary] = 1
    high = int(''.join(str(digit) for digit in high))
    low = int(''.join(str(digit) for digit in low))
    return high, low


def main():
    year, day = 2021, 24
    data = get_data(year, day)
    max_model_no, min_model_no = find_model_numbers(data)
    print(max_model_no)
    print(min_model_no)


if __name__ == "__main__":
    main()
