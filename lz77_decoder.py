import struct
import os


def decoder(input_file, output_file, max_search):
    MAX_SEARCH = max_search
    with open(input_file, "rb") as file:
        input_data = file.read()

    chararray = bytearray()
    i = 0

    while i < len(input_data):
        (offset_and_length, char) = struct.unpack(">Hc", input_data[i:i + 3])
        offset = offset_and_length >> 6
        length = offset_and_length - (offset << 6)
        i = i + 3

        if offset == 0 and length == 0:
            chararray.append(char[0])
        else:
            iterator = len(chararray) - offset
            for pointer in range(length):
                if iterator + pointer < len(chararray):
                    chararray.append(chararray[iterator + pointer])
            chararray.append(char[0])

    with open(output_file, "wb") as out_file:
        out_file.write(chararray)


def main():
    directory = 'CorpusSilesia'
    max_search = 400  # Ajuste este valor conforme necessário

    for filename in os.listdir(directory):
        if filename.startswith("compressed_") and filename.endswith(".bin") and not filename.startswith(
                "decompressed_"):
            input_file = os.path.join(directory, filename)
            original_filename = filename[len("compressed_"):-len(".bin")]
            output_file = os.path.join(directory, f"decompressed_{original_filename}")
            decoder(input_file, output_file, max_search)
            print(f"Decompressed {original_filename} successfully.")


if __name__ == "__main__":
    main()
