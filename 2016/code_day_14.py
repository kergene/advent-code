import hashlib

def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    return data

def find_keys(data):
    hashes = []
    for i in range(1000):
        key = data + str(i)
        hashed = hashlib.md5(key.encode('utf-8')).hexdigest()
        hashes.append(hashed)
    n_found = 0
    n = -1
    while n_found < 64:
        n += 1
        next_key = data + str(n + 1000)
        next_hash = hashlib.md5(next_key.encode('utf-8')).hexdigest()
        hashes.append(next_hash)
        relevant_hash = hashes[n]
        for i in range(len(relevant_hash) - 2):
            if relevant_hash[i] == relevant_hash[i+1] == relevant_hash[i+2]:
                test_char = relevant_hash[i]
                test_string = test_char * 5
                for j in range(n + 1, n + 1001):
                    if test_string in hashes[j]:
                        n_found += 1
                        break
                break
    return n

def superhash(key):
    for _ in range(2017):
        key = hashlib.md5(key.encode('utf-8')).hexdigest()
    return key

def find_superkeys(data):
    hashes = []
    for i in range(1000):
        key = data + str(i)
        hashed = superhash(key)
        hashes.append(hashed)
    n_found = 0
    n = -1
    while n_found < 64:
        n += 1
        next_key = data + str(n + 1000)
        next_hash = superhash(next_key)
        hashes.append(next_hash)
        relevant_hash = hashes[n]
        for i in range(len(relevant_hash) - 2):
            if relevant_hash[i] == relevant_hash[i+1] == relevant_hash[i+2]:
                test_char = relevant_hash[i]
                test_string = test_char * 5
                for j in range(n + 1, n + 1001):
                    if test_string in hashes[j]:
                        n_found += 1
                        break
                break
    return n

def main():
    year, day = 2016, 14
    data = get_data(year, day)
    print(find_keys(data))
    print(find_superkeys(data))

if __name__ == "__main__":
    main()
