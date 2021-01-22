def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read().split(',')
    data = [preprocess(datum) for datum in data]
    return data


def preprocess(datum):
    return int(datum)


def get_val(lines, index, parameter):
    if parameter == '1':
        return lines[index]
    else:
        return lines[lines[index]]


def set_val(lines, index, parameter, value):
    if parameter == '1':
        lines[index] = value
    else:
        lines[lines[index]] = value


def run_intcode(p_in, lines):
    i = 0
    while True:
        opcode = str(lines[i])
        instruction = int(opcode[-2:])
        params = opcode[:-2]
        if instruction == 99:
            break
        elif instruction == 1:
            param_length = 3
            params = params.zfill(param_length)
            set_val(lines, i + 3, params[-3], get_val(lines, i + 1, params[-1]) + get_val(lines, i + 2, params[-2]))
            i += param_length + 1
        elif instruction == 2:
            param_length = 3
            params = params.zfill(param_length)
            set_val(lines, i + 3, params[-3], get_val(lines, i + 1, params[-1]) * get_val(lines, i + 2, params[-2]))
            i += param_length + 1
        elif instruction == 3:
            param_length = 1
            params = params.zfill(param_length)
            set_val(lines, i + 1, params[-1], p_in)
            i += param_length + 1
        elif instruction == 4:
            param_length = 1
            params = params.zfill(param_length)
            output = get_val(lines, i + 1, params[-1])
            i += param_length + 1
        elif instruction == 5:
            param_length = 2
            params = params.zfill(param_length)
            if get_val(lines, i + 1, params[-1]):
                i = get_val(lines, i + 2, params[-2])
            else:
                i += param_length + 1
        elif instruction == 6:
            param_length = 2
            params = params.zfill(param_length)
            if not get_val(lines, i + 1, params[-1]):
                i = get_val(lines, i + 2, params[-2])
            else:
                i += param_length + 1
        elif instruction == 7:
            param_length = 3
            params = params.zfill(param_length)
            if get_val(lines, i + 1, params[-1]) < get_val(lines, i + 2, params[-2]):
                set_val(lines, i + 3, params[-3], 1)
            else:
                set_val(lines, i + 3, params[-3], 0)
            i += param_length + 1
        elif instruction == 8:
            param_length = 3
            params = params.zfill(param_length)
            if get_val(lines, i + 1, params[-1]) == get_val(lines, i + 2, params[-2]):
                set_val(lines, i + 3, params[-3], 1)
            else:
                set_val(lines, i + 3, params[-3], 0)
            i += param_length + 1
        else:
            assert False, instruction
    return output


def diagnostic(data, input_val):
    lines = data.copy()
    p_in = input_val
    return run_intcode(p_in, lines)


def main():
    year, day = 2019, 5
    data = get_data(year, day)
    print(diagnostic(data, 1))
    print(diagnostic(data, 5))


if __name__ == "__main__":
    main()
