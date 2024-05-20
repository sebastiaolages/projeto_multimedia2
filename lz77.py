import os
import time
from bitarray import bitarray


class LZ77Compressor:
    MAX_WINDOW_SIZE = 400

    def __init__(self, window_size=20):
        self.window_size = min(window_size, self.MAX_WINDOW_SIZE)
        self.lookahead_buffer_size = 15

    def compress(self, data, verbose=False):
        i = 0
        output_buffer = bitarray(endian='big')

        while i < len(data):
            match = self.findLongestMatch(data, i)

            if match:
                (bestMatchDistance, bestMatchLength) = match
                output_buffer.append(True)
                output_buffer.frombytes(bytes([bestMatchDistance >> 4]))
                output_buffer.frombytes(bytes([((bestMatchDistance & 0xf) << 4) | bestMatchLength]))
                if verbose:
                    print("<1, %i, %i>" % (bestMatchDistance, bestMatchLength), end='')
                i += bestMatchLength
            else:
                output_buffer.append(False)
                output_buffer.frombytes(bytes([data[i]]))
                if verbose:
                    print("<0, %s>" % data[i], end='')
                i += 1

        output_buffer.fill()
        return output_buffer

    def decompress(self, data):
        output_buffer = []
        bit_data = bitarray(endian='big')
        bit_data.frombytes(data)

        while len(bit_data) >= 9:
            flag = bit_data.pop(0)

            if not flag:
                byte = bit_data[0:8].tobytes()
                output_buffer.append(byte)
                del bit_data[0:8]
            else:
                byte1 = ord(bit_data[0:8].tobytes())
                byte2 = ord(bit_data[8:16].tobytes())
                del bit_data[0:16]
                distance = (byte1 << 4) | (byte2 >> 4)
                length = (byte2 & 0xf)

                for i in range(length):
                    output_buffer.append(output_buffer[-distance])

        return b''.join(output_buffer)

    def findLongestMatch(self, data, current_position):
        end_of_buffer = min(current_position + self.lookahead_buffer_size, len(data) + 1)
        best_match_distance = -1
        best_match_length = -1

        for j in range(current_position + 2, end_of_buffer):
            start_index = max(0, current_position - self.window_size)
            substring = data[current_position:j]

            for i in range(start_index, current_position):
                repetitions = len(substring) // (current_position - i)
                last = len(substring) % (current_position - i)
                matched_string = data[i:current_position] * repetitions + data[i:i + last]

                if matched_string == substring and len(substring) > best_match_length:
                    best_match_distance = current_position - i
                    best_match_length = len(substring)

        if best_match_distance > 0 and best_match_length > 0:
            return (best_match_distance, best_match_length)
        return None


def read_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except IOError:
        print(f"Could not open {file_path}")
        raise


def process_file(file_path):
    compressor = LZ77Compressor(window_size=400)
    data = read_file(file_path)
    print(f"Processando o arquivo {file_path}...")

    start_time = time.time()
    compressed_data = compressor.compress(data)
    compression_time = time.time() - start_time
    print(f"Tempo de compressão para {file_path}: {compression_time:.2f} segundos")

    compressed_size = len(compressed_data)
    original_size = len(data)
    compression_ratio = original_size / compressed_size if compressed_size else 0
    average_code_length = (compressed_size * 8) / original_size

    result = {
        'file': file_path,
        'original_size': original_size,
        'compressed_size': compressed_size,
        'compression_ratio': compression_ratio,
        'average_code_length': average_code_length,
        'compression_time': compression_time,
    }
    print(f"Resultado do arquivo {file_path}: {result}")
    return result


def process_all_files(directory_path):
    results = []
    for filename in os.listdir(directory_path):
        full_path = os.path.join(directory_path, filename)
        if os.path.isfile(full_path):
            results.append(process_file(full_path))
    return results


if __name__ == '__main__':
    directory_path = r'C:\Users\sebas\PycharmProjects\project_multimedia2\CorpusSilesia'
    results = process_all_files(directory_path)
    for result in results:
        print(result)
