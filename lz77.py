import os
import time

def lz77_encode(data, window_size=4096, lookahead_buffer_size=32):
    i = 0
    output = []
    data_length = len(data)

    while i < data_length:
        match_length = 0
        match_position = 0
        search_start = max(0, i - window_size)

        # Ajuste para garantir que não ultrapassamos o comprimento dos dados
        lookahead_limit = min(i + lookahead_buffer_size, data_length)

        for j in range(search_start, i):
            substring_length = 0
            while (i + substring_length < lookahead_limit and
                   data[j + substring_length] == data[i + substring_length]):
                substring_length += 1
            if substring_length > match_length:
                match_length = substring_length
                match_position = i - j

        # Verifique se o próximo índice é válido antes de acessar
        if i + match_length < data_length:
            next_char = data[i + match_length]
        else:
            next_char = ''

        if match_length >= 3:
            output.append((match_position, match_length, next_char))
            i += match_length + 1
        else:
            output.append((0, 0, data[i] if i < data_length else ''))
            i += 1

    return output


def lz77_decode(encoded_data):
    """
    Implementa a decodificação LZ77.
    """
    decoded = []
    for position, length, next_char in encoded_data:
        start = len(decoded) - position
        if position == 0 and length == 0:
            decoded.append(next_char)
        else:
            for _ in range(length):
                decoded.append(decoded[start])
                start += 1
            decoded.append(next_char)

    return ''.join(decoded)

def read_file_in_chunks(file_path, chunk_size=1024*1024):  # 1 MB por chunk
    print(f"Lendo o arquivo {file_path} em partes...")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            while True:
                data = file.read(chunk_size)
                if not data:
                    break
                yield data
    except UnicodeDecodeError:
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(chunk_size).decode('utf-8', errors='ignore')
                if not data:
                    break
                yield data

def process_file(file_path):
    original_size = 0
    encoded_chunks = []
    print(f"Iniciando o processamento do arquivo {file_path} em chunks...")

    for data in read_file_in_chunks(file_path):
        original_size += len(data)
        start_time = time.time()
        encoded_chunk = lz77_encode(data)
        encode_time = time.time() - start_time
        print(f"Chunk codificado em {encode_time} segundos.")
        encoded_chunks.extend(encoded_chunk)

    # Concatenando os chunks codificados para decodificação
    start_time = time.time()
    decoded_data = lz77_decode(encoded_chunks)
    decode_time = time.time() - start_time
    print(f"Tempo de decodificação: {decode_time} segundos.")

    compressed_size = sum(1 for x in encoded_chunks)  # Contagem simples de elementos
    compression_ratio = original_size / compressed_size if compressed_size else 0
    acl = (compressed_size * 8) / original_size

    return file_path, compression_ratio, acl, original_size, compressed_size

# Especificar o arquivo para processar
specific_file_path = r'C:\Users\sebas\PycharmProjects\project_multimedia2\CorpusSilesia\webster'
result = process_file(specific_file_path)
print(result)
