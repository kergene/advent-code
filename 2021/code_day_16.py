from math import prod


def get_data(year, day):
    if day < 10:
        day = '0'+str(day)
    with open(f"{year}/input_day_{day}.txt") as f:
        data = f.read()
    data = ''.join([preprocess(datum) for datum in data])
    return data


def preprocess(datum):
    return bin(int(datum,16))[2:].rjust(4,'0')


class Packet(object):
    def __init__(self, parent, version, type_id):
        self.parent = parent
        self.version = version
        self.type = type_id
        self.value = 0
        if self.type != 4:
            self.subpackets = []
        else:
            self.subpackets = None
        self.length_id = None
        self.packet_count = None
        self.bit_length = None
        self.initial_idx = None

    def count_subversions(self):
        if self.type == 4:
            return self.version
        else:
            return sum(packet.count_subversions() for packet in self.subpackets) + self.version

    def get_value(self):
        if self.type == 0:
            return sum(packet.get_value() for packet in self.subpackets)
        elif self.type == 1:
            return prod(packet.get_value() for packet in self.subpackets)
        elif self.type == 2:
            return min(packet.get_value() for packet in self.subpackets)
        elif self.type == 3:
            return max(packet.get_value() for packet in self.subpackets)
        elif self.type == 4:
            return self.value
        elif self.type == 5:
            return self.subpackets[0].get_value() > self.subpackets[1].get_value()
        elif self.type == 6:
            return self.subpackets[0].get_value() < self.subpackets[1].get_value()
        elif self.type == 7:
            return self.subpackets[0].get_value() == self.subpackets[1].get_value()


def open_packet(idx, data, parent):
    version = int(data[idx:idx + 3], 2)
    idx += 3
    type_id = int(data[idx:idx + 3], 2)
    idx += 3
    packet = Packet(parent, version, type_id)
    if packet.type != 4:
        packet.length_id = int(data[idx], 2)
        idx += 1
        if packet.length_id:
            packet.packet_count = int(data[idx:idx + 11], 2)
            idx += 11
        else:
            packet.bit_length = int(data[idx:idx + 15], 2)
            idx += 15
            packet.initial_idx = idx
    return idx, packet


def unwrap_packet(idx, data, current_packet):
    if current_packet.type == 4:
        number = []
        while int(data[idx]):
            idx += 1
            number.append(data[idx:idx + 4])
            idx += 4
        idx += 1
        number.append(data[idx:idx + 4])
        idx += 4
        current_packet.value = int(''.join(number), 2)
    else:
        if current_packet.length_id:
            for _ in range(current_packet.packet_count):
                idx, next_packet = open_packet(idx, data, current_packet)
                current_packet.subpackets.append(next_packet)
                idx = unwrap_packet(idx, data, next_packet)
        else:
            while idx - current_packet.initial_idx < current_packet.bit_length:
                idx, next_packet = open_packet(idx, data, current_packet)
                current_packet.subpackets.append(next_packet)
                idx = unwrap_packet(idx, data, next_packet)
    return idx


def sum_version_numbers(data):
    idx = 0
    idx, current_packet = open_packet(0, data, None)
    outer_packet = current_packet
    idx = unwrap_packet(idx, data, current_packet)
    return outer_packet.count_subversions()


def evaluate_transmission(data):
    idx = 0
    idx, current_packet = open_packet(0, data, None)
    outer_packet = current_packet
    idx = unwrap_packet(idx, data, current_packet)
    return outer_packet.get_value()


def main():
    year, day = 2021, 16
    data = get_data(year, day)
    print(sum_version_numbers(data))
    print(evaluate_transmission(data))


if __name__ == "__main__":
    main()
