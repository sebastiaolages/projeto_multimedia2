import struct
import os
import math


def LZ77_search(search, look_ahead):
    ls = len(search)
    llh = len(look_ahead)
    if ls == 0:
        return (0, 0, look_ahead[0:1])
    if llh == 0:
        return (-1, -1, b'')

    best_length = 0
    best_offset = 0
    buf = search + look_ahead
    search_pointer = ls

    for i in range(0, ls):
        length = 0
        while buf[i + length] == buf[search_pointer + length]:
            length += 1
            if search_pointer + length == len(buf):
                length -= 1
                break
            if i + length >= search_pointer:
                break
        if length > best_length:
            best_offset = i
            best_length = length
    return (best_offset, best_length, buf[search_pointer + best_length:search_pointer + best_length + 1])


def parse(file):
    with open(file, "rb") as f:
        return f.read()


def compress_file(input_file, output_file, max_search):
    x = 16
    max_search = int(max_search)
    max_lh = int(math.pow(2, (x - (math.log(max_search, 2)))))
    input_data = parse(input_file)

    with open(output_file, "wb") as file:
        searchiterator = 0
        lhiterator = 0

        while lhiterator < len(input_data):
            search = input_data[searchiterator:lhiterator]
            look_ahead = input_data[lhiterator:lhiterator + max_lh]
            (offset, length, char) = LZ77_search(search, look_ahead)

            shifted_offset = offset << 6
            offset_and_length = shifted_offset + length
            ol_bytes = struct.pack(">Hc", offset_and_length, bytes([char[0]]))
            file.write(ol_bytes)

            lhiterator = lhiterator + length + 1
            searchiterator = lhiterator - max_search
            if searchiterator < 0:
                searchiterator = 0


def main():
    directory = 'CorpusSilesia'
    max_search = 400  # Ajuste este valor conforme necessário

    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)) and not filename.startswith("compressed_"):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, f"compressed_{filename}.bin")
            compress_file(input_file, output_file, max_search)
            print(f"Compressed {filename} successfully.")


if __name__ == "__main__":
    main()
